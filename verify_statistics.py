import pandas as pd

# Carregar o arquivo CSV
file_path = 'performance_profiles_results.csv'
df = pd.read_csv(file_path)

# Verificar estatísticas descritivas por algoritmo e número de comparações
desc_stats = df.groupby(['Algoritmo', 'Número de Comparações'])['Erro de Estimativa'].describe()
print(desc_stats)
