import pandas as pd
import string
import json
import pymongo

def get_NCE(nces: pymongo.collection ,cod_NCE: string) -> json:
    return nces.find({"Código NCE/2023": cod_NCE})[0]

def get_requisito_academico_nce(nce: json) -> string:
    tipo = nce['Código NCE/2023'][2]
    if tipo == 'M': #denota uma vaga de mestrado
        requisito = 'Bacharelado'
    elif tipo == 'D': #denota uma vaga de doutorado
        requisito = 'Mestrado'
    else:
        requisito = -1
    
    return requisito
    
def get_requisito_posto_nce(nce: json) -> string:
    
    postos  = [posto.lstrip() for posto in nce['Posto'].split('/')]
    
    postos = ['Cap' if posto == 'Cap (Aperf)' else posto for posto in postos]
    
    return postos

def translate_posto_nce_to_portal_da_transparencia(postos: list) -> list:
    #traduz os postos da nce para os postos do portal da transparencia
    #ex: ['Cap', 'Maj'] -> ['Capitão', 'Major']

    postos_translated = []
    for posto in postos:
        if posto == 'Ten':
            postos_translated.append('Primeiro-Tenente')
            postos_translated.append('Segundo-Tenente')
        if posto == 'Cap':
            postos_translated.append('Capitão')
        elif posto == 'Maj':
            postos_translated.append('Major')
        elif posto == 'TC':
            postos_translated.append('Tenente-Coronel')
        elif posto == 'Cel':
            postos_translated.append('Coronel')
        else:
            postos_translated.append(-1)
    return postos_translated