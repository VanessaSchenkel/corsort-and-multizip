import os
import numpy as np
from scipy.stats import spearmanr
from algorithms.corsort import corsort
from algorithms.multizip_sort import multizip_sort
import logging

logging.basicConfig(level=logging.INFO)

def generate_list(size, list_type):
    if list_type == 'many_duplicates':
        return np.random.choice(range(size // 2), size).tolist()  # Muitos duplicados
    elif list_type == 'few_duplicates':
        return np.random.choice(range(size), size).tolist()  # Poucos duplicados
    elif list_type == 'no_duplicates':
        return np.random.permutation(size).tolist()  # Sem duplicados
    elif list_type == 'sorted':
        return list(range(size))  # Ordenada
    elif list_type == 'reversed':
        return list(range(size, 0, -1))  # Inversa
    else:
        raise ValueError(f"Tipo de lista desconhecido: {list_type}")

def save_list(data, file_name):
    with open(file_name, 'w') as file:
        file.write(','.join(map(str, data)))

sizes = [8, 16, 32, 64, 128, 256]
list_types = ['many_duplicates', 'few_duplicates', 'no_duplicates', 'sorted', 'reversed']
input_dir = 'data'
if not os.path.exists(input_dir):
    os.makedirs(input_dir)

for size in sizes:
    for list_type in list_types:
        file_name = os.path.join(input_dir, f'list_{list_type}_{size}.txt')
        generated_list = generate_list(size, list_type)
        save_list(generated_list, file_name)

def load_list(file_path):
    with open(file_path, 'r') as file:
        return list(map(int, file.read().strip().split(',')))

def verify_sorting(original_data, sorted_data):
    return np.array_equal(sorted(original_data), sorted_data)

def calculate_metrics(original_list, sorted_list):
    spearman_distance, _ = spearmanr(original_list, sorted_list)
    classification_error = sum(np.array(original_list) != np.array(sorted_list))
    return spearman_distance, classification_error

def save_results_incremental(result, results_file):
    with open(results_file, 'a') as file:
        file.write(f"File: {result['file_name']}\n")
        file.write(f"Corsort Correct: {result['corsort_correct']}\n")
        file.write(f"Multizip Correct: {result['multizip_correct']}\n")
        file.write(f"Corsort Comparisons: {result['corsort_comparisons']}\n")
        file.write(f"Multizip Comparisons: {result['multizip_comparisons']}\n")
        file.write(f"Spearman Distance Corsort: {result['spearman_corsort']}\n")
        file.write(f"Spearman Distance Multizip Sort: {result['spearman_multizip']}\n")
        file.write(f"Classification Error Corsort: {result['classification_error_corsort']}\n")
        file.write(f"Classification Error Multizip Sort: {result['classification_error_multizip']}\n")
        file.write("\n")

def run_tests():
    input_dir = 'data'
    result_dir = 'results'
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    logging.info(f"Procurando arquivos na pasta '{input_dir}'")

    expected_files = [f'list_{list_type}_{size}.txt' for list_type in list_types for size in sizes]

    list_files = [f for f in os.listdir(input_dir) if f in expected_files]
    
    logging.info(f"Arquivos encontrados: {list_files}")

    if not list_files:
        logging.error("Nenhum arquivo de lista encontrado.")
        return
    
    results_file = os.path.join(result_dir, 'test_results.txt')

    for file_name in list_files:
        file_path = os.path.join(input_dir, file_name)
        original_list = load_list(file_path)
        logging.info(f'Testando {file_name} com {len(original_list)} elementos.')

        sorted_corsort, corsort_comparisons = corsort(original_list.copy())
        corsort_correct = verify_sorting(original_list, sorted_corsort)
        spearman_corsort, classification_error_corsort = calculate_metrics(original_list, sorted_corsort)
        
        sorted_multizip, multizip_comparisons = multizip_sort(original_list.copy())
        multizip_correct = verify_sorting(original_list, sorted_multizip)
        spearman_multizip, classification_error_multizip = calculate_metrics(original_list, sorted_multizip)

        result = {
            'file_name': file_name,
            'corsort_correct': corsort_correct,
            'multizip_correct': multizip_correct,
            'corsort_comparisons': corsort_comparisons,
            'multizip_comparisons': multizip_comparisons,
            'spearman_corsort': spearman_corsort,
            'spearman_multizip': spearman_multizip,
            'classification_error_corsort': classification_error_corsort,
            'classification_error_multizip': classification_error_multizip,
        }

        save_results_incremental(result, results_file)

        logging.info(f"Resultados para {file_name}:")
        logging.info(f"Corsort Correct: {corsort_correct}")
        logging.info(f"Multizip Correct: {multizip_correct}")
        logging.info(f"Corsort Comparisons: {corsort_comparisons}")
        logging.info(f"Multizip Comparisons: {multizip_comparisons}")
        logging.info(f"Spearman Distance Corsort: {spearman_corsort}")
        logging.info(f"Spearman Distance Multizip Sort: {spearman_multizip}")
        logging.info(f"Classification Error Corsort: {classification_error_corsort}")
        logging.info(f"Classification Error Multizip Sort: {classification_error_multizip}")

if __name__ == "__main__":
    run_tests()
