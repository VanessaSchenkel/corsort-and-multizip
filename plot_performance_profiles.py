import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o arquivo CSV
file_path = 'performance_profiles_results.csv'
df = pd.read_csv(file_path)

# Configuração do estilo dos gráficos
sns.set(style="whitegrid")

# Calcular média e intervalos de confiança para o erro de estimativa
summary_df = df.groupby(['Algoritmo', 'Número de Comparações']).agg(
    mean_error=('Erro de Estimativa', 'mean'),
    lower=('Erro de Estimativa', lambda x: x.quantile(0.025)),
    upper=('Erro de Estimativa', lambda x: x.quantile(0.975))
).reset_index()

# Filtrar dados para gráficos
not_anytime_algorithms = ['Bubble Sort', 'Heap Sort', 'Shell Sort']
anytime_algorithms = ['Corsort', 'Merge Sort', 'Multizip Sort']

# Criar a figura e os eixos para os gráficos
fig, axes = plt.subplots(1, 2, figsize=(14, 7), sharey=True)

# Plotar algoritmos não projetados para interrupção a qualquer momento
for alg in not_anytime_algorithms:
    data = summary_df[summary_df['Algoritmo'] == alg]
    axes[0].plot(data['Número de Comparações'], data['mean_error'], label=alg)
    axes[0].fill_between(data['Número de Comparações'], data['lower'], data['upper'], alpha=0.2)

axes[0].set_title('(a) Algoritmos de ordenação não projetados para interrupção a qualquer momento')
axes[0].set_xlabel('Número k de comparações')
axes[0].set_ylabel('Erro de Estimativa S_k (normalizado)')
axes[0].set_xscale('log')
axes[0].set_yscale('log')
axes[0].legend()

# Plotar algoritmos projetados para interrupção a qualquer momento
for alg in anytime_algorithms:
    data = summary_df[summary_df['Algoritmo'] == alg]
    axes[1].plot(data['Número de Comparações'], data['mean_error'], label=alg)
    axes[1].fill_between(data['Número de Comparações'], data['lower'], data['upper'], alpha=0.2)

axes[1].set_title('(b) Algoritmos de ordenação a qualquer momento')
axes[1].set_xlabel('Número k de comparações')
axes[1].set_xscale('log')
axes[1].set_yscale('log')
axes[1].legend()

# Ajustar layout e salvar a figura
plt.tight_layout()
plt.savefig('performance_profiles_plot_updated.png')
plt.show()
