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


def get_universo_candidatos(nce: json, all_candidates: pd.DataFrame) -> list:
    # nce['patente'] = asdasd
    targetRanks = nu.translate_posto_nce_to_portal_da_transparencia(nu.get_requisito_posto_nce(nce))
    filtered = [all_candidates[
            (~all_candidates['ORG_LOTACAO'].isin(targetRanks)) &
            (all_candidates['DESCRICAO_CARGO'] == targetRank)]['NOME'] 
                 for targetRank in targetRanks]
    names = filtered['NOME'].values.tolist()
    # ids = webscraper.getNameIdsDict(names)
    # for id in ids['id']:
    #   download(id)
    #   upToMongo(id)
    return collection.find(  {"author" : { "$in": names} })

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
    


def get_score_similaridade_textual(nce: json, candidate: dict, weights: dict) -> float:
    score = 0
    keyWords = nce_utils.getKeyWords(nce)
    score += float(weights['doctorate']) * ts.get_doctorate_similarity(candidate, keyWords)
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