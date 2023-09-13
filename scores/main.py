# input: código da NCE a ser utilizada
# output: dataframe com 2 colunas: candidatos | score_candidato

import pandas as pd
import string
import json
import general_scores
import nce_utils



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
