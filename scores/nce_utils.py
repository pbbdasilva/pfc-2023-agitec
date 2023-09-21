import pandas as pd
import string
import json
import pymongo


def get_position(positions: pymongo.collection, position_id: string) -> json:
    return positions.find({"id": position_id})[0]


def get_requisito_posto_nce(position: json) -> string:
    postos = [posto.lstrip() for posto in position['rank'].split('/')]
    postos = ['Cap' if posto == 'Cap (Aperf)' else posto for posto in postos]

    return postos


def position_rank_to_transparencia(postos: list) -> list:
    # traduz os postos da nce para os postos do portal da transparencia
    # ex: ['Cap', 'Maj'] -> ['Capitão', 'Major']

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
