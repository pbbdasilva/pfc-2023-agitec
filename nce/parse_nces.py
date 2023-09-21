import pandas as pd
import camelot
import sys

def parse_nces(pdf_path):
    tables = camelot.read_pdf(pdf_path, pages='all')

    # o título está na linha 0
    # os nomes das colunas estão na linha 1
    # os nomes das colunas multilevel estão na linha 2

    # rename columns and append similar dataframes (after)
    df = tables[1].df
    df.columns = ['Código NCE/2023',
                  'OM Solicitante',
                  'Posto',
                  'Perfil',  # quadro a que o oficial pertence
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
    df = df.replace('\n', ' ', regex=True)
    df = df.replace('  ', ' ', regex=True)

    # eliminando os cabeçalhos (headers) das tabelas
    for i in range(0, len(tables)):
        # df = tables[i].df
        tables[i].df = tables[i].df.iloc[3:]

    for i in range(3, len(tables)):
        if tables[i].df[0][3] == '':
            for j in range(0, 6):
                tables[i - 1].df[j].iloc[-1:] += tables[i].df[j][3]

    # extraindo quebra de linha ---> formatação

    for i in range(3, len(tables)):
        tables[i].df = tables[i].df.replace('\n', ' ', regex=True)

    total_df_jobs = tables[3].df.append(tables[4].df)
    for i in range(5, len(tables)):
        total_df_jobs = total_df_jobs.append(tables[i].df)

    total_df_jobs = total_df_jobs.reset_index()
    total_df_jobs = total_df_jobs.drop(columns=['index'])
    total_df_jobs = total_df_jobs.drop([8, 9, 10, 11], axis=1)
    total_df_jobs.columns = ['Código NCE/2023', 'OM Solicitante', 'Posto', 'Perfil', 'Conhecimento Específico',
                             'Aplicação/Período de Aplicação do Conhecimento(PAC)', 'Instituição/Local', 'Programa',
                             'Classificação após o curso', 'Prioridade DCT']

    return total_df_jobs


if __name__ == '__main__':
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = 'sepbe51-21_port_113-dct.pdf'
    nces = parse_nces(pdf_path)
    nces.to_csv('nces.csv')