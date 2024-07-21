import csv
import matplotlib.pyplot as plt

def read_results(file_path):
    results = {
        'sizes': [],
        'corsort': {'comparisons': [], 'deviation': []},
        'multizip_sort': {'comparisons': [], 'deviation': []},
        'heap_sort': {'comparisons': [], 'deviation': []},
        'shell_sort': {'comparisons': [], 'deviation': []},
        'merge_sort': {'comparisons': [], 'deviation': []}
    }
    
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            results['sizes'].append(int(row['Tamanho da lista']))
            results['corsort']['comparisons'].append(float(row['Corsort - Média de Comparações']))
            results['corsort']['deviation'].append(float(row['Corsort - Média de Desvio relativo (%)']))
            results['multizip_sort']['comparisons'].append(float(row['Multizip Sort - Média de Comparações']))
            results['multizip_sort']['deviation'].append(float(row['Multizip Sort - Média de Desvio relativo (%)']))
            results['heap_sort']['comparisons'].append(float(row['Heap Sort - Média de Comparações']))
            results['heap_sort']['deviation'].append(float(row['Heap Sort - Média de Desvio relativo (%)']))
            results['shell_sort']['comparisons'].append(float(row['Shell Sort - Média de Comparações']))
            results['shell_sort']['deviation'].append(float(row['Shell Sort - Média de Desvio relativo (%)']))
            results['merge_sort']['comparisons'].append(float(row['Merge Sort - Média de Comparações']))
            results['merge_sort']['deviation'].append(float(row['Merge Sort - Média de Desvio relativo (%)']))
    
    return results

def generate_plot(results):
    sizes = results['sizes']
    
    plt.figure(figsize=(10, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(sizes, results['corsort']['comparisons'], label='Corsort', marker='o')
    plt.plot(sizes, results['multizip_sort']['comparisons'], label='Multizip Sort', marker='s')
    plt.plot(sizes, results['heap_sort']['comparisons'], label='Heap Sort', marker='^')
    plt.plot(sizes, results['shell_sort']['comparisons'], label='Shell Sort', marker='d')
    plt.plot(sizes, results['merge_sort']['comparisons'], label='Merge Sort', marker='x')
    plt.xlabel('Tamanho da lista')
    plt.ylabel('Média de Comparações')
    plt.title('Número Médio de Comparações')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.plot(sizes, results['corsort']['deviation'], label='Corsort', marker='o')
    plt.plot(sizes, results['multizip_sort']['deviation'], label='Multizip Sort', marker='s')
    plt.plot(sizes, results['heap_sort']['deviation'], label='Heap Sort', marker='^')
    plt.plot(sizes, results['shell_sort']['deviation'], label='Shell Sort', marker='d')
    plt.plot(sizes, results['merge_sort']['deviation'], label='Merge Sort', marker='x')
    plt.xlabel('Tamanho da lista')
    plt.ylabel('Desvio Relativo (%)')
    plt.title('Desvio Relativo Médio')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('uninterrupted_behavior_plot.png')
    plt.show()

if __name__ == "__main__":
    results_file = 'uninterrupted_behavior_results_test.csv'
    results = read_results(results_file)
    generate_plot(results)
