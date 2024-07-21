import logging
import time

logger = logging.getLogger(__name__)

def counting_sort_for_radix(arr, exp, time_limit=None, start_time=None):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    comparisons = 0

    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1
        comparisons += 1

        if time_limit and (time.time() - start_time) > time_limit:
            logger.info("Tempo limite atingido durante o Counting Sort for Radix")
            return comparisons, True

    for i in range(1, 10):
        count[i] += count[i - 1]

        if time_limit and (time.time() - start_time) > time_limit:
            logger.info("Tempo limite atingido durante o Counting Sort for Radix")
            return comparisons, True

    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
        comparisons += 1

        if time_limit and (time.time() - start_time) > time_limit:
            logger.info("Tempo limite atingido durante o Counting Sort for Radix")
            return comparisons, True

    for i in range(n):
        arr[i] = output[i]

    return comparisons, False

def radix_sort(arr, time_limit=None):
    comparisons = 0
    max_val = max(arr)
    start_time = time.time()

    exp = 1
    while max_val // exp > 0:
        comp, timeout = counting_sort_for_radix(arr, exp, time_limit, start_time)
        comparisons += comp
        if timeout:
            return arr, comparisons
        exp *= 10

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
        sorted_array, comparisons = radix_sort(test_array.copy())
        logger.info(f"Lista ordenada: {sorted_array}")
        logger.info(f"Número de comparações: {comparisons}")
        logger.info("\n")
