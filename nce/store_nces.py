import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

DB_NAME = "lattes"
COLLECTION_NAME = "positions"


class Position:
    def __init__(self, id: str, description: list[str], academic_requirement: str, rank: str):
        self.id = id
        self.description = description
        self.academic_requirement = academic_requirement
        self.rank = rank

    @property
    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "academic_requirement": self.academic_requirement,
            "rank": self.rank
        }


def get_academic_requirement(nce_id: json) -> str | None:
    if not nce_id:
        return None

    req_type = nce_id[2]
    if req_type == 'M':  # denota uma vaga de mestrado
        requirement = 'Bacharelado'
    elif req_type == 'D':  # denota uma vaga de doutorado
        requirement = 'Mestrado'
    else:
        requirement = None
    return requirement


def nce_to_position(nce) -> Position:
    description = []
    if not nce['Conhecimento Específico']:
        description.append(nce['Conhecimento Específico'])
    if not nce['Aplicação/Período de Aplicação do Conhecimento(PAC)']:
        description.append(nce['Aplicação/Período de Aplicação do Conhecimento(PAC)'])
    academic_req = get_academic_requirement(nce['Código NCE/2023'])
    return Position(nce['Código NCE/2023'], description, academic_req, nce['Posto'])


def save_position(positions):
    username = json.load(open('credentials.json'))['username']
    password = json.load(open('credentials.json'))['password']
    URI = f"mongodb+srv://{username}:{password}@lattes-pfc-2023.twn2hk2.mongodb.net/?retryWrites=true"
    client = MongoClient(URI, server_api=ServerApi('1'))
    mydb = client[DB_NAME]
    mycol = mydb[COLLECTION_NAME]
    mycol.drop()
    mycol.insert_many()


if __name__ == '__main__':
    nces = pd.read_csv('nces.csv')
    positions = [p.to_dict() for p in nces.loc[nces['Código NCE/2023'].notnull()].apply(nce_to_position, axis=1).tolist()]
    print(positions)
#    save_position(positions)
