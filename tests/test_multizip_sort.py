import sys
import os
import random
import time
from scipy.stats import rankdata
from loguru import logger
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.multizip_sort import multizip_sort

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

logger.add("logs/multizip_sort_test.log")

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

multizip_sort_results, mean_classification_error, std_classification_error, total_comparison_time = evaluate_algorithm(multizip_sort, "Multizip Sort", test_cases)

def print_results(results):
    for result in results:
        print(f"Algorithm: {result['Algorithm']}, Test Case: {result['Test Case']}")
        print(f"Original Data: {result['Original Data']}")
        print(f"Sorted Data: {result['Sorted Data']}")
        print(f"Comparisons: {result['Comparisons']}")
        print(f"Spearman Distance: {result['Spearman Distance']}")
        print(f"Classification Error: {result['Classification Error']}")
        print(f"Execution Time: {result['Execution Time']:.6f} seconds")
        print()
    
    print(f"Mean Classification Error: {mean_classification_error}")
    print(f"Standard Deviation of Classification Error: {std_classification_error}")
    print(f"Total Comparison Time: {total_comparison_time:.6f} seconds")

print_results(multizip_sort_results)
