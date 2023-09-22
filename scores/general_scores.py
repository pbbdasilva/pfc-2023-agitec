from dotenv import load_dotenv
from os import getenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from enum import Enum

load_dotenv()
weights = {
    'Linguas' : float(getenv("Linguas")),
    'PossuirMestrado' : float(getenv("PossuirMestrado")),
    'PossuirDoutorado' : float(getenv("PossuirDoutorado")),
    'NumeroDeMestrados' : float(getenv("NumeroDeMestrados")),
}

class Nivel(Enum):
    #atributos de cada linguagem
    NAO_INFORMADO = 0
    POUCO = 1
    RAZOAVELMENTE = 3
    BEM = 5


def get_language_score(cv: dict) -> float:
    #retorna a nota relacionada aos idiomas
    
    scores = []
    for language in cv['idioms']:
        reading_ability = Nivel[language['Reading']]
        speaking_ability = Nivel[language['Speaking']]
        writing_ability = Nivel[language['Writing']]
        comprehension_ability = Nivel[language['Comprehension']]
       
        score = (reading_ability.value + speaking_ability.value + writing_ability.value + comprehension_ability.value)/4
        scores.append(score)
    
    return sum(scores)/len(scores) * (1+0.1*len(scores)) #dando um peso maior para quem sabe mais idiomas


def has_masters(cv: dict) -> bool:
    #retorna se o candidato possui mestrado
    return cv['masters'] != None

def has_doctorate(cv: dict) -> bool:
    #retorna se o candidato possui doutorado
    return cv['doctorate'] != None

def get_articles_scores(cv: dict) -> float:
    #retorna a nota relacionada aos artigos
    if cv['articles'] == None:
        return 0
    else:
        return len(cv['articles'])

def get_score_geral(cv: dict) -> float:
    #retorna a nota geral do candidato
    language_score = get_language_score(cv)
    has_masters_score = int(has_masters(cv))
    has_doctorate_score = int(has_doctorate(cv))
    articles_scores = get_articles_scores(cv)
    cv['mirror'] = {}
    cv['mirror']['languages'], cv['mirror']['has_masters']= language_score, has_masters_score
    cv['mirror']['has_doctorate'], cv['mirror']['articlesNumber'] = has_doctorate_score, articles_scores
    score = 0
    score += weights['Linguas']*language_score + weights['PossuirMestrado']*has_masters_score
    score += weights['PossuirDoutorado']*has_doctorate_score + weights['NumeroDeMestrados']*articles_scores
    return score
