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
import sys

username = json.load(open('credentials.json'))['username']
password = json.load(open('credentials.json'))['password']

URI = f'''mongodb+srv://{username}:{password}@lattes-pfc-2023.twn2hk2.mongodb.net/?retryWrites=true&w=majority
'''
client = MongoClient(URI,server_api = ServerApi('1'))
database = client["lattes"]
resumes = database["resumes"]
nces = database["nce"]

def get_candidates_universe(nce: json) -> list:
    targetRanks = nu.translate_posto_nce_to_portal_da_transparencia(nu.get_requisito_posto_nce(nce))
    requirement = nu.get_requisito_academico_nce(nce)
    match requirement:
        case 'Bacharelado':
            conditions = [{'undergrad': {'$ne': None} }]
        case 'Mestrado':
            conditions = [{'masters': {'$ne': None} }]
        case _:
            conditions = []
    
    conditions.append({'rank': {'$in': targetRanks}})

    return list(resumes.find({"$and": conditions}))
    

def average(lst):
    return sum(lst) / len(lst)

def get_score_textual_similarity(nce: json, candidate: dict, weights: dict = None) -> float:
    if weights == None:
        weights = dict(pd.read_excel("defaultWeights.xlsx").to_numpy())
    score = 0
    keyWords = keyword_extraction.main(nce['Conhecimento Específico'] if nce['Conhecimento Específico'] != '' 
                                       else nce['Aplicação/Período de Aplicação do Conhecimento(PAC)'])
    score += float(weights['Doutorado']) * ts.get_doctorate_similarity(candidate, keyWords)
    score += float(weights['Mestrado']) * ts.get_masters_similarity(candidate, keyWords)
    score += float(weights['Aperfeiçoamento']) * ts.get_posgrad_similarity(candidate, keyWords)

    score += float(weights['Artigos']) * max(ts.get_articles_similarities(candidate, keyWords))
    score += float(weights['Graduação']) * max(ts.get_undergrad_similarities(candidate, keyWords))
    score += float(weights['Áreas']) * average(ts.get_areasList_similarities(candidate, keyWords))
    return 5*score

def main(cod_NCE: string) -> pd.DataFrame:
    nce = nu.get_NCE(nces,cod_NCE)
    candidatos = get_candidates_universe(nce)

    for candidato in candidatos:
        candidato['score_geral'] = get_score_geral(candidato)
        candidato['score_similaridade_textual'] = get_score_textual_similarity(nce, candidato)
        candidato['score_candidato'] = candidato['score_geral'] + candidato['score_similaridade_textual']
    
    candidatos = pd.DataFrame(candidatos)

    candidatos = candidatos.sort_values(by=['score_candidato'], ascending=False)
    
    return candidatos.loc[:,['author','score_geral', 'score_similaridade_textual', 'score_candidato']]

if __name__ == "__main__":
    if len(sys.argv) == 2:
        cod_NCE = sys.argv[1]
    else:
        cod_NCE = '13D2023'
    candidatos = main(cod_NCE)
    print(candidatos)
    
