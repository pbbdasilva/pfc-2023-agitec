import pandas as pd
import camelot
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
import sys

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


def get_nce_json(pdf_path):
    tables = camelot.read_pdf(pdf_path, pages='all')

    # o título está na linha 0
    # os nomes das colunas estão na linha 1
    # os nomes das colunas multilevel estão na linha 2

    # rename columns and append similar dataframes (after)
    df = tables[1].df
    df.columns = ['Código NCE/2023', 
                'OM Solicitante', 
                'Posto', 
                'Perfil', # quadro a que o oficial pertence
                'Conhecimento Específico',
                'Aplicação/Período de Aplicação do Conhecimento (PAC)',
                'Instituição/Local', 
                'Programa', 
                'Nível Curso',
                'OEE', 
                'Estratégia', 
                'PCM',
                'Classificação após o curso', 
                'Prioridade DCT']
    df = df.iloc[4:]

    # formatando as strings para facilitar tratamento futuro
    df = df.replace('\n',' ', regex=True)
    df = df.replace('  ',' ', regex=True)

    # eliminando os cabeçalhos (headers) das tabelas
    for i in range(0,len(tables)):
        #df = tables[i].df
        tables[i].df = tables[i].df.iloc[3:]
        
    for i in range(3,len(tables)):
        if tables[i].df[0][3] == '':
            for j in range(0,6):
                tables[i-1].df[j].iloc[-1:] += tables[i].df[j][3]

    # extraindo quebra de linha ---> formatação

    for i in range(3,len(tables)):
        tables[i].df = tables[i].df.replace('\n',' ', regex=True)
        
        
    total_df_jobs = tables[3].df.append(tables[4].df)
    for i in range(5,len(tables)):
        total_df_jobs = total_df_jobs.append(tables[i].df)
        
        
    total_df_jobs = total_df_jobs.reset_index()
    total_df_jobs = total_df_jobs.drop(columns=['index'])
    total_df_jobs = total_df_jobs.drop([8,9,10,11], axis=1)
    total_df_jobs.columns = ['Código NCE/2023','OM Solicitante','Posto','Perfil','Conhecimento Específico','Aplicação/Período de Aplicação do Conhecimento(PAC)','Instituição/Local','Programa','Classificação após o curso','Prioridade DCT']

    return total_df_jobs


def save_position(positions):
    username = json.load(open('credentials.json'))['username']
    password = json.load(open('credentials.json'))['password']
    URI = f"mongodb+srv://{username}:{password}@lattes-pfc-2023.twn2hk2.mongodb.net/?retryWrites=true"
    client = MongoClient(URI, server_api=ServerApi('1'))
    mydb = client[DB_NAME]
    mycol = mydb[COLLECTION_NAME]
    mycol.drop()
    mycol.insert_many(positions.to_dict())


if __name__ == '__main__':
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = 'sepbe51-21_port_113-dct.pdf'
    nces = get_nce_json(pdf_path)
    positions = nces.apply(nce_to_position, axis=1)
    save_position(positions)
