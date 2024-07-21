import os
import json
import time
import logging
import numpy as np
from scipy.stats import spearmanr
from algorithms.corsort import corsort
from algorithms.multizip_sort import multizip_sort

logging.basicConfig(level=logging.INFO)

data_folder = 'data'

list_sizes = [32, 64, 128, 256, 512, 1024]

num_executions = 5

def calculate_metrics(original_list, sorted_list):
    spearman_distance, _ = spearmanr(original_list, sorted_list)
    classification_error = sum(np.array(original_list) != np.array(sorted_list))
    return spearman_distance, classification_error

def test_algorithms():
    results = []
    
    files = os.listdir(data_folder)
    
    for file in files:
        file_path = os.path.join(data_folder, file)
        
        with open(file_path, 'r') as f:
            original_list = json.load(f)
        
        corsort_comparisons_list = []
        corsort_times_list = []
        corsort_spearman_list = []
        corsort_error_list = []
        
        multizip_comparisons_list = []
        multizip_times_list = []
        multizip_spearman_list = []
        multizip_error_list = []
        
        for _ in range(num_executions):
            start_time = time.time()
            corsort_result, corsort_comparisons = corsort(original_list.copy())
            corsort_time = time.time() - start_time
            corsort_spearman, corsort_error = calculate_metrics(original_list, corsort_result)
            
            corsort_comparisons_list.append(corsort_comparisons)
            corsort_times_list.append(corsort_time)
            corsort_spearman_list.append(corsort_spearman)
            corsort_error_list.append(corsort_error)
            
            start_time = time.time()
            multizip_result, multizip_comparisons = multizip_sort(original_list.copy())
            multizip_time = time.time() - start_time
            multizip_spearman, multizip_error = calculate_metrics(original_list, multizip_result)
            
            multizip_comparisons_list.append(multizip_comparisons)
            multizip_times_list.append(multizip_time)
            multizip_spearman_list.append(multizip_spearman)
            multizip_error_list.append(multizip_error)
        
        results.append({
            'file': file,
            'corsort_correct': corsort_result == sorted(original_list),
            'multizip_correct': multizip_result == sorted(original_list),
            'corsort_comparisons_avg': np.mean(corsort_comparisons_list),
            'multizip_comparisons_avg': np.mean(multizip_comparisons_list),
            'corsort_time_avg': np.mean(corsort_times_list),
            'multizip_time_avg': np.mean(multizip_times_list),
            'corsort_spearman_avg': np.mean(corsort_spearman_list),
            'multizip_spearman_avg': np.mean(multizip_spearman_list),
            'corsort_error_avg': np.mean(corsort_error_list),
            'multizip_error_avg': np.mean(multizip_error_list)
        })
    
    with open('results.json', 'w') as f:
        json.dump(results, f, indent=4)
    
    logging.info("Testes concluídos e resultados salvos.")

if __name__ == '__main__':
    test_algorithms()
