import logging
import time

logger = logging.getLogger(__name__)

def bubble_sort(arr, time_limit=None):
    comparisons = 0
    n = len(arr)
    start_time = time.time()
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if time_limit is not None and (time.time() - start_time) > time_limit:
                logger.info("Tempo limite atingido, interrompendo Bubble Sort")
                return arr, comparisons
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr, comparisons

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    test_cases = [
        ("Caso 1 - Aleatório Pequeno", [3, 6, 8, 10, 1, 2, 1]),
        ("Caso 2 - Ordenado", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ("Caso 3 - Invertido", [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]),
        ("Caso 4 - Duplicados", [4, 1, 3, 4, 1, 2, 4, 3]),
        ("Caso 5 - Todos Iguais", [5, 5, 5, 5, 5, 5, 5, 5]),
        ("Caso 6 - Aleatório Médio", [3, 6, 2, 8, 4, 7, 5, 1, 9, 0]),
        ("Caso 7 - Aleatório Grande", [87, 53, 10, 34, 95, 89, 22, 18, 80, 60, 66, 90, 71, 17, 71, 93, 68, 6, 54, 76]),
    ]

    for case_name, test_array in test_cases:
        logger.info(f"--- {case_name} ---")
        logger.info(f"Lista original: {test_array}")
        sorted_array, comparisons = bubble_sort(test_array.copy(), time_limit=1)
        logger.info(f"Lista ordenada: {sorted_array}")
        logger.info(f"Número de comparações: {comparisons}")
        logger.info("\n")
