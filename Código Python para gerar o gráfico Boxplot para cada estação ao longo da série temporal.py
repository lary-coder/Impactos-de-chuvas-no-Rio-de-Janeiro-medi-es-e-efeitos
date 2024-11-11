import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Criar uma coluna de datas (mês/ano) com base nas colunas
dados_estacoes.columns = pd.to_datetime(dados_estacoes.columns, format='%d/%m/%Y')

# Transformar os dados no formato longo para o Seaborn
dados_longos = pd.melt(dados_estacoes.T, var_name='Estação', value_name='Precipitação')
dados_longos['Estação'] = estacoes.repeat(dados_estacoes.shape[1]).values
dados_longos = dados_longos.reset_index().rename(columns={'index': 'Data'})  # Index é a data (mês/ano)

# Expurgar os outliers acima de 500
dados_longos_sem_outliers = dados_longos[dados_longos['Precipitação'] <= 500]

# Gerar o boxplot sem outliers
plt.figure(figsize=(16, 8))
sns.boxplot(x='Estação', y='Precipitação', data=dados_longos_sem_outliers)
plt.title('Boxplot de Precipitação por Estação (2014-2024)')
plt.xticks(rotation=90)  # Rotacionar os nomes das estações para facilitar a leitura
plt.xlabel('Estação')
plt.ylabel('Precipitação')
plt.tight_layout()  # Ajustar layout para que os rótulos não fiquem sobrepostos
plt.show()

# Identificar os maiores valores de cada estação
maiores_valores = dados_longos.groupby('Estação').apply(lambda x: x.loc[x['Precipitação'].idxmax()])

# Converter a coluna Data para datetime se não estiver no formato correto
maiores_valores['Data'] = pd.to_datetime(maiores_valores['Data'], errors='coerce')

# Converter a coluna Data para o formato mês/ano
maiores_valores['Data'] = maiores_valores['Data'].dt.strftime('%m/%Y')

# Exibir o mês/ano dos maiores valores por estação
print(maiores_valores[['Estação', 'Data', 'Precipitação']])
