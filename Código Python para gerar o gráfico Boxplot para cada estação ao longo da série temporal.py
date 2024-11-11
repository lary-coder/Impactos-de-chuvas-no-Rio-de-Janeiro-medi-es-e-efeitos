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


# As colunas representam as datas no cabeçalho, então formatamos as colunas corretamente
dados_estacoes.columns = pd.to_datetime(df.columns[1:], format='%d/%m/%Y')


# Criar um dataframe com as estações como índice
dados_estacoes.index = estacoes


# Identificar os maiores valores de cada estação (por linha)
maiores_valores = dados_estacoes.idxmax(axis=1)  # Retorna o mês/ano com o maior valor para cada estação
precipitacao_maxima = dados_estacoes.max(axis=1)  # Retorna o maior valor de precipitação para cada estação


# Converter as datas de maiores_valores para o formato datetime
maiores_valores = pd.to_datetime(maiores_valores)


# Combinar as informações de data (mês/ano) e os valores máximos em um dataframe
resultados = pd.DataFrame({
    'Estação': estacoes,
    'Data': maiores_valores.dt.strftime('%m/%Y'),  # Formatar para mês/ano
    'Precipitação Máxima': precipitacao_maxima
})


# Exibir o resultado final
print(resultados)


# Plotar o gráfico boxplot com os valores máximos marcados
dados_longos = pd.melt(dados_estacoes.T, var_name='Estação', value_name='Precipitação')
dados_longos['Estação'] = estacoes.repeat(dados_estacoes.shape[1]).values


# Expurgar os outliers acima de 500
dados_longos_sem_outliers = dados_longos[dados_longos['Precipitação'] <= 500]


# Gerar o boxplot sem outliers
plt.figure(figsize=(16, 8))
sns.boxplot(x='Estação', y='Precipitação', data=dados_longos_sem_outliers)


# Marcar os maiores valores de precipitação no gráfico
sns.scatterplot(x='Estação', y='Precipitação', data=resultados, color='red', s=100, label='Maior valor')


# Adicionar rótulos de mês/ano para os maiores valores
for i in range(resultados.shape[0]):
    plt.text(i, resultados['Precipitação Máxima'].iloc[i] + 5,
             resultados['Data'].iloc[i],
             horizontalalignment='center', size='small', color='black', weight='semibold')


# Ajustes no gráfico
plt.title('Boxplot de Precipitação por Estação (2014-2024) com Maiores Valores')
plt.xticks(rotation=90)  # Rotacionar os nomes das estações para facilitar a leitura
plt.xlabel('Estação')
plt.ylabel('Precipitação')
plt.tight_layout()  # Ajustar layout para que os rótulos não fiquem sobrepostos
plt.legend()
plt.show()


