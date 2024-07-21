import logging
import time

logger = logging.getLogger(__name__)

def counting_sort(arr, time_limit=None):
    comparisons = 0
    start_time = time.time()
    
    max_val = max(arr)
    min_val = min(arr)
    range_of_elements = max_val - min_val + 1

    count = [0] * range_of_elements
    output = [0] * len(arr)

    for i in range(len(arr)):
        if time_limit is not None and (time.time() - start_time) > time_limit:
            logger.info("Tempo limite atingido, interrompendo Counting Sort")
            return arr, comparisons
        count[arr[i] - min_val] += 1
        comparisons += 1

    for i in range(1, len(count)):
        if time_limit is not None and (time.time() - start_time) > time_limit:
            logger.info("Tempo limite atingido, interrompendo Counting Sort")
            return arr, comparisons
        count[i] += count[i - 1]

    for i in range(len(arr) - 1, -1, -1):
        if time_limit is not None and (time.time() - start_time) > time_limit:
            logger.info("Tempo limite atingido, interrompendo Counting Sort")
            return arr, comparisons
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1

    for i in range(len(arr)):
        if time_limit is not None and (time.time() - start_time) > time_limit:
            logger.info("Tempo limite atingido, interrompendo Counting Sort")
            return arr, comparisons
        arr[i] = output[i]

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
        sorted_array, comparisons = counting_sort(test_array.copy(), time_limit=1)
        logger.info(f"Lista ordenada: {sorted_array}")
        logger.info(f"Número de comparações: {comparisons}")
        logger.info("\n")
