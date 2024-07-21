import random
import math
import csv
from algorithms.corsort import corsort
from algorithms.multizip_sort import multizip_sort
from algorithms.heap_sort import heap_sort
from algorithms.shell_sort import shell_sort
from algorithms.merge_sort import merge_sort

# Função para gerar listas aleatórias
def generate_random_lists(sizes, num_lists=50):
    random_lists = {size: [] for size in sizes}
    for size in sizes:
        for _ in range(num_lists):
            random_lists[size].append([random.randint(0, 1000) for _ in range(size)])
    return random_lists

# Função para calcular o limite inferior teórico
def theoretical_lower_bound(n):
    return n * math.log2(n) - n / math.log(2) + math.log2(2 * math.pi * n) / 2

# Função para calcular o desvio relativo
def relative_deviation(comparisons, n):
    lower_bound = theoretical_lower_bound(n)
    return (comparisons - lower_bound) / lower_bound * 100

# Tamanhos das listas a serem geradas
sizes = [8, 16, 32, 64, 128, 256, 512, 1024]
num_lists = 50

# Gerar listas aleatórias
random_lists = generate_random_lists(sizes, num_lists)

# Resultados
results = {size: {'corsort': [], 'multizip_sort': [], 'heap_sort': [], 'shell_sort': [], 'merge_sort': []} for size in sizes}

for size in sizes:
    for lst in random_lists[size]:
        # Corsort
        sorted_data, corsort_comparisons = corsort(lst.copy())
        results[size]['corsort'].append(corsort_comparisons)

        # Multizip Sort
        sorted_data, multizip_sort_comparisons = multizip_sort(lst.copy())
        results[size]['multizip_sort'].append(multizip_sort_comparisons)

        # Heap Sort
        sorted_data, heap_sort_comparisons = heap_sort(lst.copy())
        results[size]['heap_sort'].append(heap_sort_comparisons)

        # Shell Sort
        sorted_data, shell_sort_comparisons = shell_sort(lst.copy())
        results[size]['shell_sort'].append(shell_sort_comparisons)

        # Merge Sort
        sorted_data, merge_sort_comparisons = merge_sort(lst.copy())
        results[size]['merge_sort'].append(merge_sort_comparisons)

# Calcular os desvios relativos
deviations = {size: {'corsort': [], 'multizip_sort': [], 'heap_sort': [], 'shell_sort': [], 'merge_sort': []} for size in sizes}

for size in sizes:
    for corsort_comparisons, multizip_sort_comparisons, heap_sort_comparisons, shell_sort_comparisons, merge_sort_comparisons in zip(
        results[size]['corsort'], results[size]['multizip_sort'], results[size]['heap_sort'], results[size]['shell_sort'], results[size]['merge_sort']):
        
        corsort_deviation = relative_deviation(corsort_comparisons, size)
        multizip_sort_deviation = relative_deviation(multizip_sort_comparisons, size)
        heap_sort_deviation = relative_deviation(heap_sort_comparisons, size)
        shell_sort_deviation = relative_deviation(shell_sort_comparisons, size)
        merge_sort_deviation = relative_deviation(merge_sort_comparisons, size)

        deviations[size]['corsort'].append(corsort_deviation)
        deviations[size]['multizip_sort'].append(multizip_sort_deviation)
        deviations[size]['heap_sort'].append(heap_sort_deviation)
        deviations[size]['shell_sort'].append(shell_sort_deviation)
        deviations[size]['merge_sort'].append(merge_sort_deviation)

# Calcular médias e intervalos de confiança
mean_results = {size: {'corsort': {}, 'multizip_sort': {}, 'heap_sort': {}, 'shell_sort': {}, 'merge_sort': {}} for size in sizes}

for size in sizes:
    mean_results[size]['corsort']['comparisons'] = sum(results[size]['corsort']) / num_lists
    mean_results[size]['corsort']['deviation'] = sum(deviations[size]['corsort']) / num_lists
    mean_results[size]['multizip_sort']['comparisons'] = sum(results[size]['multizip_sort']) / num_lists
    mean_results[size]['multizip_sort']['deviation'] = sum(deviations[size]['multizip_sort']) / num_lists
    mean_results[size]['heap_sort']['comparisons'] = sum(results[size]['heap_sort']) / num_lists
    mean_results[size]['heap_sort']['deviation'] = sum(deviations[size]['heap_sort']) / num_lists
    mean_results[size]['shell_sort']['comparisons'] = sum(results[size]['shell_sort']) / num_lists
    mean_results[size]['shell_sort']['deviation'] = sum(deviations[size]['shell_sort']) / num_lists
    mean_results[size]['merge_sort']['comparisons'] = sum(results[size]['merge_sort']) / num_lists
    mean_results[size]['merge_sort']['deviation'] = sum(deviations[size]['merge_sort']) / num_lists

# Nome do arquivo CSV
csv_file = 'uninterrupted_behavior_results.csv'

# Salvar resultados em um arquivo CSV
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Tamanho da lista', 'Corsort - Média de Comparações', 'Corsort - Média de Desvio relativo (%)',
                     'Multizip Sort - Média de Comparações', 'Multizip Sort - Média de Desvio relativo (%)',
                     'Heap Sort - Média de Comparações', 'Heap Sort - Média de Desvio relativo (%)',
                     'Shell Sort - Média de Comparações', 'Shell Sort - Média de Desvio relativo (%)',
                     'Merge Sort - Média de Comparações', 'Merge Sort - Média de Desvio relativo (%)'])
    
    for size in sizes:
        writer.writerow([size, mean_results[size]['corsort']['comparisons'], mean_results[size]['corsort']['deviation'],
                         mean_results[size]['multizip_sort']['comparisons'], mean_results[size]['multizip_sort']['deviation'],
                         mean_results[size]['heap_sort']['comparisons'], mean_results[size]['heap_sort']['deviation'],
                         mean_results[size]['shell_sort']['comparisons'], mean_results[size]['shell_sort']['deviation'],
                         mean_results[size]['merge_sort']['comparisons'], mean_results[size]['merge_sort']['deviation']])

print(f"Resultados de teste salvos em '{csv_file}'")
