# input: código da NCE a ser utilizada
# output: dataframe com 2 colunas: candidatos | score_candidato

import pandas as pd
import string
import json
from scores import general_scores

def get_NCE(nces: json,cod_NCE: string) -> json:
    for nce in nces:
        if nce['Código NCE/2023'] == cod_NCE:
            return nce
    return -1

def get_requisito_academico_nce(nce: json) -> string:
    tipo = nce['Código NCE/2023'][2]
    if tipo == 'M':
        requisito = 'Bacharelado'
    elif tipo == 'D':
        requisito = 'Mestrado'
    else:
        requisito = -1
    
    return requisito
    
def get_requisito_posto_nce(nce: json) -> string:
    requisito_postos  = nce['Posto'].strip



def get_universo_candidatos(nce: json, all_candidates: pd.DataFrame) -> pd.DataFrame:
    
    requisito = get_requisito_academico_nce(nce)

    
def get_score_geral(nce: json, candidato:pd.Series) -> float:
    

def get_score_similaridade_textual(nce: json, candidato:pd.Series) -> float:
    pass

def get_score_candidato(nce: json) -> pd.DataFrame:
    pass

def main(cod_NCE: string) -> pd.DataFrame:
    nce = get_NCE(cod_NCE)
    candidatos = get_universo_candidatos(nce)
    candidatos['score_geral'] = candidatos.apply(lambda x: get_score_geral(nce, x), axis=1)
    candidatos['score_similaridade_textual'] = candidatos.apply(lambda x: get_score_similaridade_textual(nce, x), axis=1)
    candidatos['score_candidato'] = candidatos['score_geral'] + candidatos['score_similaridade_textual']