import pandas as pd


# Carregar o arquivo Excel
file_path = '/content/drive/MyDrive/Python/Chuva-AlertaRJ_2014-2024.xlsx'
df = pd.read_excel(file_path, sheet_name='Mensal_2014-2024')


# Definir o intervalo de linhas que contém as estações (2 até 33)
estacoes_df = df.iloc[1:33, :]  # Seleciona as linhas 2 até 33 (índice 1 até 32 em Python)


# Definir o nome da coluna que contém os nomes das estações (coluna A)
estacao_col = df.columns[0]  # Assumindo que a coluna A é a primeira, ou seja, índice 0


# Separar a coluna de estações das demais colunas
estacoes = estacoes_df[estacao_col]
dados_estacoes = estacoes_df.drop(columns=[estacao_col])


# Calcular as estatísticas para cada estação
estatisticas = pd.DataFrame({
    'Média': dados_estacoes.mean(axis=1),
    'Moda': dados_estacoes.mode(axis=1)[0],
    'Mediana': dados_estacoes.median(axis=1),
    'Desvio Padrão': dados_estacoes.std(axis=1),
    'Coeficiente de Variação (%)': (dados_estacoes.std(axis=1) / dados_estacoes.mean(axis=1)) * 100
})


# Adicionar o nome das estações ao DataFrame de estatísticas
estatisticas.index = estacoes
estatisticas.index.name = 'Estação'


print(estatisticas)
