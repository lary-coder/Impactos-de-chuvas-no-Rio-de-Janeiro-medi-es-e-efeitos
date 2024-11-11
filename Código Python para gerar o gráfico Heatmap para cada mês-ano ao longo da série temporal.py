import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Carregar os dados da planilha Excel
file_path = '/content/drive/MyDrive/Python/Chuva-AlertaRJ_2014-2024.xlsx'
df = pd.read_excel(file_path, sheet_name='Mensal_2014-2024')


# Exibir as primeiras linhas do DataFrame para inspecionar os dados
print(df.head())


# Remover a coluna 'Estação' se quiser calcular a média de todas as estações
df.set_index('Estação', inplace=True)


# Converter as colunas de datas para o formato datetime
df.columns = pd.to_datetime(df.columns)


# Agora vamos calcular a média de todas as estações por mês/ano
df_media = df.mean(axis=0).reset_index()
df_media.columns = ['Data', 'Valor Médio']


# Extraímos o ano e o mês
df_media['Ano'] = df_media['Data'].dt.year
df_media['Mês'] = df_media['Data'].dt.month


# Pivotar para criar a tabela com anos como linhas e meses como colunas
df_pivot = df_media.pivot(index='Ano', columns='Mês', values='Valor Médio')


# Arredondar os valores para inteiros (usando .round() para evitar NaN)
df_pivot = df_pivot.round().fillna(0).astype(int)


# Renomear os meses para as abreviações
meses = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
df_pivot.columns = meses


# Plotar o heatmap com números inteiros
plt.figure(figsize=(12, 8))
sns.heatmap(df_pivot, annot=True, cmap='coolwarm', cbar=True, fmt="d")
plt.title('Heatmap de Médias Mensais por Ano (2014-2024)')
plt.xlabel('Meses')
plt.ylabel('Anos')
plt.show()
