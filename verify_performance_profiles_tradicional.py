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
        try:
            result = compare_fn(X, compare=compare, max_comparisons=max_comparisons, *args, **kwargs)
        except RuntimeError:
            result = X  # Retorna a lista até o ponto de interrupção
        return result, wrapper.count
    return wrapper

@count_comparisons
def heap_sort(X, compare, max_comparisons):
    logger.info("Iniciando Heap Sort")

    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and compare(arr[largest], arr[l]):
            largest = l
        if r < n and compare(arr[largest], arr[r]):
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(X)
    for i in range(n // 2 - 1, -1, -1):
        heapify(X, n, i)
    try:
        for i in range(n - 1, 0, -1):
            if heap_sort.count > max_comparisons:
                break
            X[i], X[0] = X[0], X[i]
            heapify(X, i, 0)
    except RuntimeError:
        pass

    logger.info("Heap Sort concluído")
    return X

@count_comparisons
def shell_sort(X, compare, max_comparisons):
    logger.info("Iniciando Shell Sort")
    n = len(X)
    gap = n // 2
    try:
        while gap > 0:
            for i in range(gap, n):
                temp = X[i]
                j = i
                while j >= gap and compare(X[j - gap], temp):
                    if shell_sort.count > max_comparisons:
                        raise RuntimeError("Número máximo de comparações atingido")
                    X[j] = X[j - gap]
                    j -= gap
                X[j] = temp
            gap //= 2
    except RuntimeError:
        pass
    logger.info("Shell Sort concluído")
    return X

@count_comparisons
def merge_sort(X, compare, max_comparisons):
    logger.info("Iniciando Merge Sort")

    def merge(arr, l, m, r):
        n1 = m - l + 1
        n2 = r - m
        L = arr[l:m+1]
        R = arr[m+1:r+1]
        i = j = 0
        k = l
        while i < n1 and j < n2:
            if merge_sort.count > max_comparisons:
                raise RuntimeError("Número máximo de comparações atingido")
            if compare(R[j], L[i]):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1

    def merge_sort_recursive(arr, l, r):
        if l < r:
            m = l + (r - l) // 2
            merge_sort_recursive(arr, l, m)
            merge_sort_recursive(arr, m + 1, r)
            merge(arr, l, m, r)

    try:
        merge_sort_recursive(X, 0, len(X) - 1)
    except RuntimeError:
        pass
    logger.info("Merge Sort concluído")
    return X

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
        for algo_fn, algo_name in [(heap_sort, 'Heap Sort'), (shell_sort, 'Shell Sort'), (merge_sort, 'Merge Sort')]:
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
    save_results_to_csv(results, 'performance_profiles_tradicional.csv')

if __name__ == "__main__":
    main()
