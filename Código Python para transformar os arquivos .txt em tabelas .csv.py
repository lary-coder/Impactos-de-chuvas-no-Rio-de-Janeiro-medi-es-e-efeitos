import pandas as pd
import zipfile
import os


# Caminho para o arquivo ZIP
zip_file_path = '/content/drive/MyDrive/Python/ChuvasRJ/DadosPluviometricos2020_csv.zip'


# Diretório temporário para extrair os arquivos
extract_dir = '/content/drive/MyDrive/Python/ChuvasRJ/temp/'


# Extraia os arquivos CSV do ZIP
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)


# Inicialize um dicionário para armazenar os totais
data_totals = {}


# Iterar sobre os arquivos extraídos
for file_name in os.listdir(extract_dir):
    if file_name.endswith('.csv'):
        # Ler o arquivo CSV
        df = pd.read_csv(os.path.join(extract_dir, file_name))


        # Verificar se a coluna "15 min" existe
        if '15 min' in df.columns:
            # Transformar os valores da coluna "15 min" em float e calcular o total
            total = df['15 min'].apply(pd.to_numeric, errors='coerce').sum()


            # Extrair o nome da linha e da coluna a partir do nome do arquivo
            line_name = file_name.split('_')[0]
            col_name = file_name.split('_')[1].replace('.csv', '')


            # Adicionar ao dicionário
            if line_name not in data_totals:
                data_totals[line_name] = {}
            data_totals[line_name][col_name] = total


# Converter o dicionário em um DataFrame
result_df = pd.DataFrame(data_totals).T


# Exportar para um arquivo Excel
result_df.to_excel('/content/drive/MyDrive/Python/ChuvasRJ/DadosPluviométricos2020.xlsx', index=True)


print("Arquivo DadosPluviométricos2024.xlsx criado com sucesso!")
