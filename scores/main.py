# input: código da NCE a ser utilizada
# output: dataframe com 2 colunas: candidatos | score_candidato

import argparse
import json
import keyword_extraction
import nce_utils as nu
import pandas as pd
import string
import text_similarity_scores as ts

from dotenv import load_dotenv
from general_scores import get_score_geral
from os import getenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


load_dotenv()
weights = {
    'Doutorado' : float(getenv("Doutorado")),
    'Mestrado' : float(getenv("Mestrado")),
    'Aperfeicoamento' : float(getenv("Aperfeicoamento")),
    'Graduacao' : float(getenv("Graduacao")),
    'Artigos' : float(getenv("Artigos")),
    'Areas' : float(getenv("Areas")),
}
username = json.load(open('credentials.json'))['username']
password = json.load(open('credentials.json'))['password']

URI = f"mongodb+srv://{username}:{password}@lattes-pfc-2023.twn2hk2.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(URI, server_api=ServerApi('1'))
database = client["lattes"]
resumes = database["resumes"]
positions = database["positions"]


def get_candidates_universe(position: json) -> list:
    targetRanks = nu.position_rank_to_transparencia(nu.get_requisito_posto_nce(position))
    requirement = position['academic_requirement']
    match requirement:
        case 'Bacharelado':
            conditions = [{'undergrad': {'$ne': None}}]
        case 'Mestrado':
            conditions = [{'masters': {'$ne': None}}]
        case _:
            conditions = []
    conditions.append({'rank': {'$in': targetRanks}})

    return list(resumes.find({"$and": conditions}))


def average(lst):
    return sum(lst) / len(lst)


def get_score_textual_similarity(position: json, candidate: dict) -> float:
    score = 0
    keyWords = keyword_extraction.main(position['description'][0])
    candidate.setdefault('mirror',{})

    doctorate_sim = ts.get_doctorate_similarity(candidate, keyWords)
    candidate['mirror']['doctorate_sim'] = doctorate_sim
    score += float(weights['Doutorado']) * doctorate_sim

    masters_sim = ts.get_masters_similarity(candidate, keyWords)
    candidate['mirror']['masters_sim'] = masters_sim
    score += float(weights['Mestrado']) * masters_sim

    posgrad_sim =  ts.get_posgrad_similarity(candidate, keyWords)
    candidate['mirror']['posgrad_sim'] = posgrad_sim
    score += float(weights['Aperfeicoamento']) *posgrad_sim

    articles_sim = ts.get_articles_similarities(candidate, keyWords)
    articles_sim_max = max(articles_sim)
    candidate['mirror']['articles_sim'] = articles_sim
    candidate['mirror']['articles_sim_max'] = articles_sim_max
    score += float(weights['Artigos']) * articles_sim_max

    undergrad_sim = ts.get_undergrad_similarities(candidate, keyWords)
    undergrad_sim_max = max(undergrad_sim)
    candidate['mirror']['undergrad_sim'] = undergrad_sim
    candidate['mirror']['undergrad_sim_max'] = undergrad_sim_max
    score += float(weights['Graduacao']) * undergrad_sim_max

    areasList_sim = ts.get_areasList_similarities(candidate, keyWords)
    areasList_sim_avr = average(areasList_sim)
    candidate['mirror']['areasList_sim'] = areasList_sim
    candidate['mirror']['areasList_sim_avr'] = areasList_sim_avr
    score += float(weights['Areas']) * areasList_sim_avr

    return score


def main(position_id: string) -> pd.DataFrame:
    position = nu.get_position(positions, position_id)
    candidates = get_candidates_universe(position)

    for candidate in candidates:
        candidate['score_geral'] = get_score_geral(candidate)
        candidate['score_similaridade_textual'] = get_score_textual_similarity(position, candidate)
        candidate['score_candidato'] = candidate['score_geral'] + candidate['score_similaridade_textual']
    candidates = pd.DataFrame(candidates).sort_values(by=['score_candidato'], ascending=False)

    return candidates.loc[:, ['author', 'score_geral', 'score_similaridade_textual', 'score_candidato']]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rank candidate for given position')
    parser.add_argument('--id', help='Position id')
    args = parser.parse_args()
    position_id = args.id
    if not position_id:
        position_id = '13D2023'
    candidates_ranking = main(position_id)
    print(candidates_ranking)
