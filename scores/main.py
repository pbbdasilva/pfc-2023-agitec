# input: código da NCE a ser utilizada
# output: dataframe com 2 colunas: candidatos | score_candidato

import pandas as pd
import string
import json
from general_scores import get_score_geral
import nce_utils as nu
import keyword_extraction
import text_similarity_scores as ts
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

username = json.load(open('scores/credentials.json'))['username']
password = json.load(open('scores/credentials.json'))['password']

URI = f'''mongodb+srv://{username}:{password}@lattes-pfc-2023.twn2hk2.mongodb.net/?retryWrites=true&w=majority
'''
client = MongoClient(URI,server_api = ServerApi('1'))
database = client["lattes"]
resumes = database["resumes"]
nces = database["nce"]

all_candidates = pd.read_csv('./scores/202301_Cadastro.csv', sep=';', engine='python', encoding = 'latin1')

def get_candidates_universe(nce: json, all_candidates: pd.DataFrame) -> list:
    targetRanks = nu.translate_posto_nce_to_portal_da_transparencia(nu.get_requisito_posto_nce(nce))
    requirement = nu.get_requisito_academico_nce(nce)
    filtered = all_candidates[
            (all_candidates['ORG_LOTACAO'] == 'Comando do Exército') &
            (all_candidates['DESCRICAO_CARGO'].isin(targetRanks))]['NOME'] 
    names = filtered.values.tolist()
    names = [name.title() for name in names]
    match requirement:
        case 'Bacharelado':
            conditions = [{"author" : { "$in": names} }, {'undergrad': {'$ne': None} }]
        case 'Mestrado':
            conditions = [{"author" : { "$in": names} }, {'masters': {'$ne': None} }]
        case _:
            conditions = [{"author" : { "$in": names} }]
    return list(resumes.find({"$and": conditions}))
    

def average(lst):
    return sum(lst) / len(lst)

def get_score_textual_similarity(nce: json, candidate: dict, weights: dict = None) -> float:
    if weights == None:
        weights = dict(pd.read_excel("scores/defaultWeights.xlsx").to_numpy())
    score = 0
    keyWords = keyword_extraction.main(nce['Conhecimento Específico'] if nce['Conhecimento Específico'] != '' 
                                       else nce['Aplicação/Período de Aplicação do Conhecimento(PAC)'])
    score += float(weights['Doutorado']) * ts.get_doctorate_similarity(candidate, keyWords)
    score += float(weights['Mestrado']) * ts.get_masters_similarity(candidate, keyWords)
    score += float(weights['Aperfeiçoamento']) * ts.get_posgrad_similarity(candidate, keyWords)

    score += float(weights['Artigos']) * max(ts.get_articles_similarities(candidate, keyWords))
    score += float(weights['Graduação']) * max(ts.get_undergrad_similarities(candidate, keyWords))
    score += float(weights['Áreas']) * average(ts.get_areasList_similarities(candidate, keyWords))
    return score

def main(cod_NCE: string) -> pd.DataFrame:
    nce = nu.get_NCE(nces,cod_NCE)
    candidatos = get_candidates_universe(nce,all_candidates)
    
    for candidato in candidatos:
        candidato['score_geral'] = get_score_geral(candidato)
        candidato['score_similaridade_textual'] = get_score_textual_similarity(nce, candidato)
        candidato['score_candidato'] = candidato['score_geral'] + candidato['score_similaridade_textual']
    return candidatos

#exemplo de chamada
candidatos = main('13D2023')
print(candidatos)