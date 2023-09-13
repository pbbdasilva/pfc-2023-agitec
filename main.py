# input: código da NCE a ser utilizada
# output: dataframe com 2 colunas: candidatos | score_candidato

import pandas as pd
import string
import json
from scores import general_scores
from scores import text_similarity_scores as ts
from nce_etl import nce_utils as nu, keyword_extraction
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

username = json.load(open('credentials.json'))['username']
password = json.load(open('credentials.json'))['password']

URI = f'''mongodb+srv://{username}:{password}@lattes-pfc-2023.twn2hk2.mongodb.net/?retryWrites=true&w=majority
'''
client = MongoClient(URI,server_api = ServerApi('1'))
database = client["lattes"]
resumes = database["resumes"]

def get_universo_candidatos(nce: json, all_candidates: pd.DataFrame) -> pd.DataFrame:
    pass

def get_universe_candidates(nce: json, all_candidates: pd.DataFrame) -> list:
    targetRanks = nu.translate_posto_nce_to_portal_da_transparencia(nu.get_requisito_posto_nce(nce))
    filtered = all_candidates[
            (all_candidates['ORG_LOTACAO'] == 'Comando do Exército') &
            (all_candidates['DESCRICAO_CARGO'].isin(targetRanks))]['NOME'] 
    names = filtered.values.tolist()
    names = [name.title() for name in names]
    return list(collection.find({"author" : { "$in": names} }))
    


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
    return score

    # ts.get_articles_similarities(candidate, keyWords)
    # ts.get_undergrad_similarities(candidate, keyWords)
    # ts.get_areasList_similarities(candidate, keyWords)
    # ts.get_doctorate_similarity(candidate, keyWords)
    # ts.get_posgrad_similarity(candidate, keyWords)
    # ts.get_masters_similarity(candidate, ["Computação", "Segurança", "Leis", "Legislação", "Redigir"])
    # return 0

def get_score_candidato(nce: json) -> pd.DataFrame:
    pass

def main(cod_NCE: string) -> pd.DataFrame:
    nce = nu.get_NCE(cod_NCE)
    candidatos = get_universo_candidatos(nce)
    candidatos['score_geral'] = candidatos.apply(lambda x: general_scores.get_score_geral(x), axis=1)
    candidatos['score_similaridade_textual'] = candidatos.apply(lambda x: get_score_similaridade_textual(nce, x), axis=1)
    candidatos['score_candidato'] = candidatos['score_geral'] + candidatos['score_similaridade_textual']