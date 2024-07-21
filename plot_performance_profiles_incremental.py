import matplotlib.pyplot as plt
import pandas as pd

# Carregar dados dos CSVs
incremental_data = pd.read_csv('performance_profiles_incremental.csv', header=None, names=['List_Index', 'Algorithm', 'Comparisons', 'Used_Comparisons', 'Estimation_Error'])
traditional_data = pd.read_csv('performance_profiles_tradicional.csv', header=None, names=['List_Index', 'Algorithm', 'Comparisons', 'Used_Comparisons', 'Estimation_Error'])

# Separar os dados por algoritmo para incremental_data
corsort_data = incremental_data[incremental_data['Algorithm'] == 'Corsort']
multizip_sort_data = incremental_data[incremental_data['Algorithm'] == 'Multizip Sort']

# Separar os dados por algoritmo para traditional_data
heap_sort_data = traditional_data[traditional_data['Algorithm'] == 'Heap Sort']
shell_sort_data = traditional_data[traditional_data['Algorithm'] == 'Shell Sort']
merge_sort_data = traditional_data[traditional_data['Algorithm'] == 'Merge Sort']

# Agregar os resultados para Corsort
aggregated_corsort = corsort_data.groupby('Comparisons')['Estimation_Error'].agg(['mean', 'std'])

# Agregar os resultados para Multizip Sort
aggregated_multizip = multizip_sort_data.groupby('Comparisons')['Estimation_Error'].agg(['mean', 'std'])

# Agregar os resultados para Heap Sort
aggregated_heap = heap_sort_data.groupby('Comparisons')['Estimation_Error'].agg(['mean', 'std'])

# Agregar os resultados para Shell Sort
aggregated_shell = shell_sort_data.groupby('Comparisons')['Estimation_Error'].agg(['mean', 'std'])

# Agregar os resultados para Merge Sort
aggregated_merge = merge_sort_data.groupby('Comparisons')['Estimation_Error'].agg(['mean', 'std'])

# Plotar o gráfico com linha contínua para Corsort
plt.errorbar(aggregated_corsort.index, aggregated_corsort['mean'], yerr=aggregated_corsort['std'], fmt='-o', capsize=5, linestyle='-', marker='o', label='Corsort')

# Plotar o gráfico com linha contínua para Multizip Sort
plt.errorbar(aggregated_multizip.index, aggregated_multizip['mean'], yerr=aggregated_multizip['std'], fmt='-s', capsize=5, linestyle='-', marker='s', label='Multizip Sort')

# Plotar o gráfico com linha contínua para Heap Sort
plt.errorbar(aggregated_heap.index, aggregated_heap['mean'], yerr=aggregated_heap['std'], fmt='-^', capsize=5, linestyle='-', marker='^', label='Heap Sort')

# Plotar o gráfico com linha contínua para Shell Sort
plt.errorbar(aggregated_shell.index, aggregated_shell['mean'], yerr=aggregated_shell['std'], fmt='-v', capsize=5, linestyle='-', marker='v', label='Shell Sort')

# Plotar o gráfico com linha contínua para Merge Sort
plt.errorbar(aggregated_merge.index, aggregated_merge['mean'], yerr=aggregated_merge['std'], fmt='-x', capsize=5, linestyle='-', marker='x', label='Merge Sort')

plt.xlabel('Number of Comparisons')
plt.ylabel('Normalized Estimation Error')
plt.title('Performance Profiles')
plt.legend()
plt.grid(True)

# Salvar o gráfico na pasta 'images'
plt.savefig('images/performance_profiles.png')

# Mostrar o gráfico
plt.show()
