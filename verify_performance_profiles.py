import csv
import random
import time
from loguru import logger
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def count_comparisons(compare_fn):
    def wrapper(X, *args, max_comparisons=None, **kwargs):
        wrapper.count = 0
        def compare(a, b):
            wrapper.count += 1
            if max_comparisons and wrapper.count > max_comparisons:
                raise RuntimeError("Número máximo de comparações atingido")
            return a < b
        result = compare_fn(X, compare=compare, max_comparisons=max_comparisons, *args, **kwargs)
        return result, wrapper.count
    return wrapper

@count_comparisons
def corsort(X, compare, max_comparisons):
    logger.info("Iniciando Corsort")
    n = len(X)
    M = np.eye(n)

    def update_partial_order(M, i, j):
        M[i, j] = 1
        M[j, i] = -1
        descendants_i = np.where(M[:, i] == 1)[0]
        ascendants_j = np.where(M[j, :] == 1)[0]
        for k in descendants_i:
            for l in ascendants_j:
                M[k, l] = 1
                M[l, k] = -1
        return M

    def compute_estimators(M):
        d = np.sum(M == 1, axis=0)
        a = np.sum(M == 1, axis=1)
        return d - a, d / (d + a)

    def choose_next_comparison(M, delta, I):
        S = np.argwhere(M == 0)
        i, j = min(S, key=lambda pair: (abs(delta[pair[0]] - delta[pair[1]]), max(I[pair[0]], I[pair[1]])))
        return i, j

    delta, rho = compute_estimators(M)
    while np.any(M == 0):
        try:
            I = delta + np.sum(M == 1, axis=0) + np.sum(M == 1, axis=1)
            i, j = choose_next_comparison(M, delta, I)
            if not compare(X[i], X[j]):
                i, j = j, i
            M = update_partial_order(M, i, j)
            delta, rho = compute_estimators(M)
        except RuntimeError:
            logger.error("Número máximo de comparações atingido")
            break
    sorted_list = [x for _, x in sorted(zip(rho, X))]
    logger.info("Corsort concluído")
    return sorted_list

@count_comparisons
def multizip_sort(X, compare, max_comparisons):
    def split(arrs):
        logger.debug(f"Dividindo: {arrs}")
        new_arrs = []
        for arr in arrs:
            mid = len(arr) // 2
            new_arrs.append(arr[:mid])
            new_arrs.append(arr[mid:])
        return new_arrs

    def multizip_merge(arrs):
        while len(arrs) > 1:
            new_arrs = []
            for i in range(0, len(arrs), 2):
                if i + 1 < len(arrs):
                    new_arrs.append(merge(arrs[i], arrs[i + 1]))
                else:
                    new_arrs.append(arrs[i])
            arrs = new_arrs
        if arrs:
            return arrs[0]
        return []

    def merge(arr1, arr2):
        result = []
        i = j = 0
        while i < len(arr1) and j < len(arr2):
            try:
                if compare(arr1[i], arr2[j]):
                    result.append(arr1[i])
                    i += 1
                else:
                    result.append(arr2[j])
                    j += 1
            except RuntimeError:
                logger.error("Número máximo de comparações atingido no merge")
                result.extend(arr1[i:])
                result.extend(arr2[j:])
                break
        result.extend(arr1[i:])
        result.extend(arr2[j:])
        return result

    logger.info("Iniciando Multizip Sort")
    arrs = [X]
    try:
        while any(len(sub_arr) > 1 for sub_arr in arrs):
            arrs = split(arrs)
    except RuntimeError:
        logger.error("Número máximo de comparações atingido durante o split")
    sorted_arr = multizip_merge(arrs)
    logger.info("Multizip Sort concluído")
    return sorted_arr

def generate_random_lists(num_lists, list_size):
    return [random.sample(range(list_size * 10), list_size) for _ in range(num_lists)]

def calculate_estimation_error(sorted_list):
    n = len(sorted_list)
    error = 0
    for i in range(n):
        for j in range(i + 1, n):
            if sorted_list[i] > sorted_list[j]:
                error += 1
    max_error = n * (n - 1) / 2
    normalized_error = error / max_error
    return normalized_error

def run_experiments(data_lists, max_comparisons_list):
    results = []
    for list_idx, data in enumerate(data_lists):
        for algo_fn, algo_name in [(corsort, 'Corsort'), (multizip_sort, 'Multizip Sort')]:
            for comparisons in max_comparisons_list:
                try:
                    sorted_data, used_comparisons = algo_fn(data.copy(), max_comparisons=comparisons)
                    estimation_error = calculate_estimation_error(sorted_data)
                    results.append((list_idx, algo_name, comparisons, used_comparisons, estimation_error))
                    logger.info(f"{algo_name} completado com {used_comparisons} comparações e erro de estimação {estimation_error:.6f}.")
                except RuntimeError as e:
                    logger.error(f"Erro ao executar o algoritmo {algo_name} com {comparisons} comparações: {str(e)}")
                    estimation_error = calculate_estimation_error(data)
                    results.append((list_idx, algo_name, comparisons, comparisons, estimation_error))
    return results

def save_results_to_csv(results, filename):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(results)

def main():
    num_lists = 50
    list_size = 150
    max_comparisons = [200, 400, 600, 800]

    data_lists = generate_random_lists(num_lists, list_size)
    results = run_experiments(data_lists, max_comparisons)
    save_results_to_csv(results, 'performance_profiles_incremental.csv')

if __name__ == "__main__":
    main()
