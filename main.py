# input: código da NCE a ser utilizada
# output: dataframe com 2 colunas: candidatos | score_candidato

import pandas as pd
import string
import json

def get_NCE(cod_NCE: string) -> json:
    pass

def get_universo_candidatos(nce: json) -> pd.DataFrame:
    pass

def get_score_geral(nce: json, candidato:pd.Series) -> float:
    pass

def get_score_similaridade_textual(nce: json, candidato:pd.Series) -> float:
    pass

def get_score_candidato(nce: json) -> pd.DataFrame:
    pass