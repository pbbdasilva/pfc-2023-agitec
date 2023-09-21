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
import argparse

username = json.load(open('credentials.json'))['username']
password = json.load(open('credentials.json'))['password']

URI = f"mongodb+srv://{username}:{password}@lattes-pfc-2023.twn2hk2.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(URI, server_api=ServerApi('1'))
database = client["lattes"]
resumes = database["resumes"]
positions = database["positions"]


def get_candidates_universe(position: json) -> list:
    targetRanks = nu.position_rank_to_transparencia(nu.get_requisito_posto_nce(position))
    requirement = position['rank']
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


def get_score_textual_similarity(position: json, candidate: dict, weights: dict = None) -> float:
    if weights is None:
        weights = dict(pd.read_excel("defaultWeights.xlsx").to_numpy())
    score = 0
    keyWords = keyword_extraction.main(position['description'][0])
    score += float(weights['Doutorado']) * ts.get_doctorate_similarity(candidate, keyWords)
    score += float(weights['Mestrado']) * ts.get_masters_similarity(candidate, keyWords)
    score += float(weights['Aperfeiçoamento']) * ts.get_posgrad_similarity(candidate, keyWords)

    score += float(weights['Artigos']) * max(ts.get_articles_similarities(candidate, keyWords))
    score += float(weights['Graduação']) * max(ts.get_undergrad_similarities(candidate, keyWords))
    score += float(weights['Áreas']) * average(ts.get_areasList_similarities(candidate, keyWords))

    return 5 * score


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
