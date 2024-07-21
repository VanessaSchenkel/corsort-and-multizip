import numpy as np
from loguru import logger
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def spearmans_footrule(X, sorted_X):
    if len(X) != len(sorted_X):
        raise ValueError("Deve ter o mesmo tamanho")

    rank_X = {val: idx for idx, val in enumerate(X)}
    rank_sorted_X = {val: idx for idx, val in enumerate(sorted_X)}

    logger.info(f"Original list: {X}")
    logger.info(f"Sorted list: {sorted_X}")
    logger.info(f"Rank of original list: {rank_X}")
    logger.info(f"Rank of sorted list: {rank_sorted_X}")

    error = sum(abs(rank_X[val] - rank_sorted_X[val]) for val in X if val in rank_sorted_X)
    
    logger.info(f"Spearman's footrule error: {error}")
    return error

def performance_profile(algorithm, data, steps=10):
    n = len(data)
    sorted_data = sorted(data)
    step_size = max(len(data) // steps, 1)
    performance = []

    for k in range(step_size, len(data) + 1, step_size):
        partial_data, comparisons = algorithm(data[:k])
        error = spearmans_footrule(partial_data, sorted_data[:k])
        performance.append((k, error, comparisons))
    
    return performance

def compute_variance(errors):
    return np.var(errors)

if __name__ == "__main__":
    logger.add("logs/app.log")

    sample_data = [5, 1, 8, 7, 2, 6, 4, 3]
    sorted_sample_data = sorted(sample_data)

    error = spearmans_footrule(sample_data, sorted_sample_data)
    logger.info(f"Spearman's footrule error: {error}")

    from algorithms.corsort import corsort
    performance = performance_profile(corsort, sample_data)
    logger.info(f"Performance profile: {performance}")

    errors = [error for _, error, _ in performance]
    variance = compute_variance(errors)
    logger.info(f"Variance of errors: {variance}")

    from algorithms.merge_sort import merge_sort
    from algorithms.insertion_sort import insertion_sort
    from algorithms.heap_sort import heap_sort

    test_cases = {
        "Caso 1": ([5, 3, 4, 2, 1], [1, 2, 3, 4, 5]),
        "Caso 2": ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        "Caso 3": ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
        "Caso 4": ([3, 1, 4, 2, 5], [1, 2, 3, 4, 5])
    }

    for case_name, (unsorted_list, sorted_list) in test_cases.items():
        logger.info(f"Testando {case_name}")
        spearman_error = spearmans_footrule(unsorted_list, sorted_list)
        logger.info(f"{case_name} - Spearman's footrule error: {spearman_error}")

    sorted_data, comparisons_merge = merge_sort(sample_data)
    logger.info(f"Merge Sort - Lista ordenada: {sorted_data}, Número de comparações: {comparisons_merge}")

    sorted_data, comparisons_insertion = insertion_sort(sample_data)
    logger.info(f"Insertion Sort - Lista ordenada: {sorted_data}, Número de comparações: {comparisons_insertion}")

    sorted_data, comparisons_heap = heap_sort(sample_data)
    logger.info(f"Heap Sort - Lista ordenada: {sorted_data}, Número de comparações: {comparisons_heap}")

    performance_merge = performance_profile(merge_sort, sample_data)
    logger.info(f"Performance profile (Merge Sort): {performance_merge}")

    performance_insertion = performance_profile(insertion_sort, sample_data)
    logger.info(f"Performance profile (Insertion Sort): {performance_insertion}")

    performance_heap = performance_profile(heap_sort, sample_data)
    logger.info(f"Performance profile (Heap Sort): {performance_heap}")

    errors_merge = [error for _, error, _ in performance_merge]
    variance_merge = compute_variance(errors_merge)
    logger.info(f"Variance of errors (Merge Sort): {variance_merge}")

    errors_insertion = [error for _, error, _ in performance_insertion]
    variance_insertion = compute_variance(errors_insertion)
    logger.info(f"Variance of errors (Insertion Sort): {variance_insertion}")

    errors_heap = [error for _, error, _ in performance_heap]
    variance_heap = compute_variance(errors_heap)
    logger.info(f"Variance of errors (Heap Sort): {variance_heap}")

    large_sample_data = np.random.randint(1, 1000, 100).tolist()
    large_sorted_data = sorted(large_sample_data)

    large_error = spearmans_footrule(large_sample_data, large_sorted_data)
    logger.info(f"Spearman's footrule error for large data: {large_error}")

    large_performance = performance_profile(corsort, large_sample_data)
    logger.info(f"Performance profile for large data (Corsort): {large_performance}")

    large_errors = [error for _, error, _ in large_performance]
    large_variance = compute_variance(large_errors)
    logger.info(f"Variance of errors for large data: {large_variance}")
