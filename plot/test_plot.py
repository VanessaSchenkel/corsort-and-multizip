import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

overhead_df = pd.read_csv('results/uninterrupted_behavior_with_overhead.csv')
results_df = pd.read_csv('results/uninterrupted_behavior_results.csv')

algorithms = overhead_df['algorithm'].unique()
print(f"Algoritmos encontrados: {algorithms}")

missing_data = []
for size in overhead_df['list_size'].unique():
    for algo in algorithms:
        if overhead_df[(overhead_df['list_size'] == size) & (overhead_df['algorithm'] == algo)].empty:
            missing_data.append((algo, size))

if missing_data:
    print("Dados faltando para os seguintes algoritmos e tamanhos de lista:")
    for algo, size in missing_data:
        print(f"Algoritmo: {algo}, Tamanho da Lista: {size}")
else:
    print("Todos os dados estão presentes.")

plt.figure(figsize=(10, 6))
sns.lineplot(data=overhead_df, x='list_size', y='relative_overhead', hue='algorithm', marker='o')
plt.yscale('log')
plt.title('Overhead Relativo dos Algoritmos de Ordenação')
plt.xlabel('Tamanho da Lista')
plt.ylabel('Overhead Relativo (%)')
plt.legend(title='Algoritmo')
plt.grid(True, which="both", ls="--")
plt.savefig('images/overhead_relativo.png')
plt.show()

plt.figure(figsize=(10, 6))
sns.lineplot(data=results_df, x='list_size', y='time', hue='algorithm', marker='o')
plt.yscale('log')
plt.title('Tempo de Execução Médio dos Algoritmos de Ordenação')
plt.xlabel('Tamanho da Lista')
plt.ylabel('Tempo de Execução Médio (s)')
plt.legend(title='Algoritmo')
plt.grid(True, which="both", ls="--")
plt.savefig('images/tempo_execucao_medio.png')
plt.show()
