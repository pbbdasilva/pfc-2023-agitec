import requests as req
import argparse
import os
from io import BytesIO
import zipfile
import pandas as pd

ranks = {'Soldado-Recruta', 'Aluno Org Formacao Oficiais Reserva', 'Segundo-Tenente',
         'Cabo (engajado)', 'Terceiro-Sargento', 'Primeiro-Tenente', 'Soldado',
         'Subtenente', 'Capitao', 'Major','Segundo-Sargento', 'Primeiro-Sargento',
         'Coronel', 'Tenente-Coronel', 'Aluno Escola Formacao Sargentos',
         'Cadete AMAN/Aluno IME(demais anos)', 'Aspirante-a-Oficial',
         'General-de-Exercito', 'Aluno da Escola Cadetes(ultimo ano)',
         'General-de-Brigada', 'General-de-Divisao', 'Taifeiro-Mor',
         'Cadete AMAN/Aluno IME(ultimo ano)'}
rankErrorMessage = r'''invalid rank. The available ranks are: 'Soldado-Recruta' 'Aluno Org Formacao Oficiais Reserva'
                    'Segundo-Tenente' 'Cabo (engajado)' 'Terceiro-Sargento' 'Primeiro-Tenente' 'Soldado'
                    'Subtenente' 'Capitao' 'Major' 'Segundo-Sargento' 'Primeiro-Sargento' 'Coronel'
                    'Tenente-Coronel' 'Aluno Escola Formacao Sargentos' 'Cadete AMAN/Aluno IME(demais anos)'
                    'Aspirante-a-Oficial' 'General-de-Exercito' 'Aluno da Escola Cadetes(ultimo ano)'
                    'General-de-Brigada''General-de-Divisao''Taifeiro-Mor''Cadete AMAN/Aluno IME(ultimo ano)'
                    '''

url = "https://portaldatransparencia.gov.br/download-de-dados/servidores/"

def filter_candidates(month, year):
    df = pd.read_csv(year + month + "_Cadastro.csv", encoding = "ISO-8859-1", sep=';', engine='python')
    filtered = df[(df['ORG_LOTACAO'] == 'Comando do Exército') & (df['DESCRICAO_CARGO'].isin(ranks))].loc[:,['NOME', 'DESCRICAO_CARGO']]
    filtered.to_excel(year + month + "Army.xlsx", index=False)

def fetch(url):
    try:
        r = req.get(url)
    except req.exceptions.ConnectionError as e:
        print(e)
    if r.status_code != 200:
        print("error for {}".format(url))
    return r

def fetch_candidates(month, year):
    # check if already have file for given date
    if year + month + "_Cadastro.csv" in os.listdir(os.getcwd()):
        print("Already have candidates file.....skipping fetch from " + url)
        return

    response = fetch(url + year + month + "_Militares")
    if not response:
        return
    zip_content = BytesIO(response.content)
    with zipfile.ZipFile(zip_content, 'r') as zip_ref:
        zip_ref.extractall()
    print("Fetched and unzipped candidates file")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch candidates from portal da transparencia')
    parser.add_argument('--month', help='Month parameter')
    parser.add_argument('--year', help='Month parameter')
    args = parser.parse_args()
    month = args.month
    year = args.year

    if not month or not year:
        print("Error: Month (--month) and Year (--year) parameters are required.")
        print("Month should be used as MM (e.g. January is 01)")
        exit(1)
    fetch_candidates(month, year)
    filter_candidates(month, year)