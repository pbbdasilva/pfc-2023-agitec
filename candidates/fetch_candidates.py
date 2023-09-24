import requests as req
import argparse
import os
from io import BytesIO
import zipfile
import pandas as pd

ranks = {'Segundo-Tenente','Primeiro-Tenente', 'Subtenente', 'Capitao', 
         'Major', 'Coronel', 'Tenente-Coronel', 'Aspirante-a-Oficial',
         'General-de-Exercito', 'General-de-Brigada', 'General-de-Divisao',
        }
rankErrorMessage = r'''invalid rank. The available ranks are: 'Soldado-Recruta' 'Aluno Org Formacao Oficiais Reserva'
                    'Segundo-Tenente' 'Cabo (engajado)' 'Terceiro-Sargento' 'Primeiro-Tenente' 'Soldado'
                    'Subtenente' 'Capitao' 'Major' 'Segundo-Sargento' 'Primeiro-Sargento' 'Coronel'
                    'Tenente-Coronel' 'Aluno Escola Formacao Sargentos' 'Cadete AMAN/Aluno IME(demais anos)'
                    'Aspirante-a-Oficial' 'General-de-Exercito' 'Aluno da Escola Cadetes(ultimo ano)'
                    'General-de-Brigada''General-de-Divisao''Taifeiro-Mor''Cadete AMAN/Aluno IME(ultimo ano)'
                    '''

url = "https://portaldatransparencia.gov.br/download-de-dados/servidores/"
user_agent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0'}

def filter_candidates(month, year):
    try:
        df = pd.read_csv(year + month + "_Cadastro.csv", encoding = "ISO-8859-1", sep=';', engine='python')
        filtered = df[(df['ORG_LOTACAO'] == 'Comando do Exército') & (df['DESCRICAO_CARGO'].isin(ranks))].loc[:,['NOME', 'DESCRICAO_CARGO']]
        filtered.to_excel(year + month + "Army.xlsx", index=False)
    except FileNotFoundError as e:
        print("run --fetch True")
def fetch(url):
    try:
        r = req.get(url, headers=user_agent)
    except req.exceptions.ConnectionError as e:
        print(e)
    if r.status_code != 200:
        print("error {} for {}".format(r.status_code, url))
    return r

def fetch_candidates(month, year, force_fetch):
    # check if already have file for given date
    if year + month + "_Cadastro.csv" in os.listdir(os.getcwd()) and not force_fetch:
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
    parser.add_argument("--fetch", type=bool, default=False, help="Force fetch from url even with local files")
    args = parser.parse_args()
    month = args.month
    year = args.year
    force_fetch = args.fetch

    if not month or not year:
        print("Error: Month (--month) and Year (--year) parameters are required.")
        print("Month should be used as MM (e.g. January is 01)")
        exit(1)
    fetch_candidates(month, year, force_fetch)
    filter_candidates(month, year)

