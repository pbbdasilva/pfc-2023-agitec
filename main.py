# input: código da NCE a ser utilizada
# output: dataframe com 2 colunas: candidatos | score_candidato

import pandas as pd
import string
import json
from scores import general_scores
from nce_etl import nce_utils


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

    


def get_score_similaridade_textual(nce: json, candidato:pd.Series) -> float:
    return 0

def get_score_candidato(nce: json) -> pd.DataFrame:
    pass

def main(cod_NCE: string) -> pd.DataFrame:
    nce = nce_utils.get_NCE(cod_NCE)
    candidatos = get_universo_candidatos(nce)
    candidatos['score_geral'] = candidatos.apply(lambda x: general_scores.get_score_geral(x), axis=1)
    candidatos['score_similaridade_textual'] = candidatos.apply(lambda x: get_score_similaridade_textual(nce, x), axis=1)
    candidatos['score_candidato'] = candidatos['score_geral'] + candidatos['score_similaridade_textual']