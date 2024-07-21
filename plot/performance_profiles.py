import os
import sys
import time
import csv
from loguru import logger

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from algorithms.corsort import corsort
from algorithms.multizip_sort import multizip_sort
from algorithms.quick_sort import quick_sort
from algorithms.bubble_sort import bubble_sort
from algorithms.heap_sort import heap_sort
from algorithms.insertion_sort import insertion_sort
from algorithms.merge_sort import merge_sort
from algorithms.selection_sort import selection_sort
from algorithms.shell_sort import shell_sort
from algorithms.radix_sort import radix_sort
from algorithms.counting_sort import counting_sort

# Configuração do logger
logger.add("logs/performance_profiles.log", level="INFO")

def load_list_from_file(file_path):
    with open(file_path, 'r') as f:
        return [int(item) for item in f.readline().strip().split(',')]

def save_results_incrementally(file_path, results):
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(results)

def test_performance_profiles():
    data_folder = 'data'
    file_paths = [os.path.join(data_folder, file) for file in os.listdir(data_folder) if file.endswith('.txt')]
    logger.info(f"Arquivos encontrados: {file_paths}")

    time_limits = [0.001, 0.01, 0.1, 1, 10]  # 1ms, 10ms, 100ms, 1s, 10s
    algorithms = {
        "corsort": corsort,
        "multizip_sort": multizip_sort,
        "quick_sort": quick_sort,
        "bubble_sort": bubble_sort,
        "heap_sort": heap_sort,
        "insertion_sort": insertion_sort,
        "merge_sort": merge_sort,
        "selection_sort": selection_sort,
        "shell_sort": shell_sort,
        "radix_sort": radix_sort,
        "counting_sort": counting_sort,
    }

    for file_path in file_paths:
        original_list = load_list_from_file(file_path)
        file_name = os.path.basename(file_path)

        for time_limit in time_limits:
            result = {
                "file": file_name,
                "time_limit": time_limit,
            }

            for algo_name, algo_func in algorithms.items():
                start_time = time.time()
                sorted_result, comparisons = algo_func(original_list.copy(), time_limit=time_limit)
                duration = time.time() - start_time
                result[f"{algo_name}_duration"] = duration
                result[f"{algo_name}_comparisons"] = comparisons

            logger.info(f"Resultados para {file_name} com limite de tempo {time_limit}s: {result}")
            save_results_incrementally('results/performance_profiles_results.csv', result)

if __name__ == "__main__":
    test_performance_profiles()
