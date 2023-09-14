from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from enum import Enum
 

class Nivel(Enum):
    #atributos de cada linguagem
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
    return get_language_score(cv) + int(has_masters(cv)) + int(has_doctorate(cv)) + get_articles_scores(cv)