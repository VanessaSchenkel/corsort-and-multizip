import sys
import os
import random
import time
import csv
from scipy.stats import rankdata
from loguru import logger
import numpy as np

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

def spearman_footrule_distance(X, Y):
    X_rank = rankdata(X)
    Y_rank = rankdata(Y)
    return np.sum(np.abs(X_rank - Y_rank))

def classification_error(X, Y):
    error = 0
    for i, y in enumerate(Y):
        if y != X[i]:
            error += 1
    return error

log_file = "results/compare_sorts.log"
logger.add(log_file, level="INFO")

test_cases = {
    f"Lista {i}": [random.randint(0, 100) for _ in range(random.randint(10, 50))]
    for i in range(1, 21)
}

def evaluate_algorithm(algorithm, algorithm_name, test_cases):
    results = []
    comparison_times = []
    classification_errors = []
    
    for description, sample_data in test_cases.items():
        start_time = time.time()
        sorted_data, num_comparisons = algorithm(sample_data.copy())
        end_time = time.time()
        
        spearman_distance = spearman_footrule_distance(sample_data, sorted_data)
        classification_error_value = classification_error(sample_data, sorted_data)
        
        comparison_time = end_time - start_time
        comparison_times.append(comparison_time)
        classification_errors.append(classification_error_value)
        
        results.append({
            "Algorithm": algorithm_name,
            "Test Case": description,
            "Original Data": sample_data,
            "Sorted Data": sorted_data,
            "Comparisons": num_comparisons,
            "Spearman Distance": spearman_distance,
            "Classification Error": classification_error_value,
            "Execution Time": comparison_time
        })
        logger.info(f"{algorithm_name} - {description}: Comparisons: {num_comparisons}, "
                    f"Spearman Distance: {spearman_distance}, "
                    f"Classification Error: {classification_error_value}, "
                    f"Execution Time: {comparison_time:.6f} seconds")
    
    mean_classification_error = np.mean(classification_errors)
    std_classification_error = np.std(classification_errors)
    total_comparison_time = np.sum(comparison_times)
    
    logger.info(f"{algorithm_name} - Metrics Summary: "
                f"Mean Classification Error: {mean_classification_error}, "
                f"Standard Deviation of Classification Error: {std_classification_error}, "
                f"Total Comparison Time: {total_comparison_time:.6f} seconds")
    
    return results, mean_classification_error, std_classification_error, total_comparison_time

algorithms = [
    (corsort, "Corsort"),
    (multizip_sort, "Multizip Sort"),
    (quick_sort, "Quick Sort"),
    (bubble_sort, "Bubble Sort"),
    (heap_sort, "Heap Sort"),
    (insertion_sort, "Insertion Sort"),
    (merge_sort, "Merge Sort"),
    (selection_sort, "Selection Sort"),
    (shell_sort, "Shell Sort"),
    (radix_sort, "Radix Sort"),
    (counting_sort, "Counting Sort")
]

all_results = []
for algorithm, name in algorithms:
    results, mean_ce, std_ce, total_time = evaluate_algorithm(algorithm, name, test_cases)
    all_results.append((name, results, mean_ce, std_ce, total_time))

def print_results(results, mean_ce, std_ce, total_time):
    for result in results:
        print(f"Algorithm: {result['Algorithm']}, Test Case: {result['Test Case']}")
        print(f"Original Data: {result['Original Data']}")
        print(f"Sorted Data: {result['Sorted Data']}")
        print(f"Comparisons: {result['Comparisons']}")
        print(f"Spearman Distance: {result['Spearman Distance']}")
        print(f"Classification Error: {result['Classification Error']}")
        print(f"Execution Time: {result['Execution Time']:.6f} seconds")
        print()
    
    print(f"Mean Classification Error: {mean_ce}")
    print(f"Standard Deviation of Classification Error: {std_ce}")
    print(f"Total Comparison Time: {total_time:.6f} seconds")

def save_results_to_csv(all_results, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ["Algorithm", "Test Case", "Comparisons", "Spearman Distance", "Classification Error", "Execution Time"]
        writer.writerow(header)
        
        for name, results, _, _, _ in all_results:
            for result in results:
                writer.writerow([result['Algorithm'], result['Test Case'], result['Comparisons'], result['Spearman Distance'], result['Classification Error'], result['Execution Time']])

output_csv = os.path.join('results', 'comparison_results.csv')
save_results_to_csv(all_results, output_csv)

print(f"Results saved to {output_csv}")

for name, results, mean_ce, std_ce, total_time in all_results:
    print(f"Results for {name}:")
    print_results(results, mean_ce, std_ce, total_time)

def compare_results(all_results):
    for i in range(len(test_cases)):
        test_case_name = all_results[0][1][i]['Test Case']
        print(f"Comparing {test_case_name}:")
        for name, results, _, _, _ in all_results:
            result = results[i]
            print(f"{name} - Comparisons: {result['Comparisons']}, Spearman Distance: {result['Spearman Distance']}, Classification Error: {result['Classification Error']}, Execution Time: {result['Execution Time']:.6f} seconds")
        print()

compare_results(all_results)

with open('results/compare_sorts_log.txt', 'w') as f:
    with open(log_file, 'r') as log_f:
        f.write(log_f.read())
