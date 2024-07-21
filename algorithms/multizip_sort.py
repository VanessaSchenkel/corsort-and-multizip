import time
import logging

logging.basicConfig(level=logging.INFO)

def multizip_sort(arr, time_limit=None):
    start_time = time.time()
    comparisons = 0

    def compare(a, b):
        nonlocal comparisons
        comparisons += 1
        return a < b

    def split(arrs):
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
                    new_arrs.append(merge(arrs[i], arrs[i+1]))
                else:
                    new_arrs.append(arrs[i])
            arrs = new_arrs
        return arrs[0]

    def merge(arr1, arr2):
        result = []
        i = j = 0
        while i < len(arr1) and j < len(arr2):
            if compare(arr1[i], arr2[j]):
                result.append(arr1[i])
                i += 1
            else:
                result.append(arr2[j])
                j += 1
        result.extend(arr1[i:])
        result.extend(arr2[j:])
        return result

    logging.info("Iniciando Multizip Sort")
    arrs = [arr]
    while any(len(sub_arr) > 1 for sub_arr in arrs):
        arrs = split(arrs)
        if time_limit and (time.time() - start_time) >= time_limit:
            break
    sorted_arr = multizip_merge(arrs)
    logging.info("Multizip Sort concluído")
    return sorted_arr, comparisons

if __name__ == "__main__":
    test_cases = [
        ("Aleatório Pequeno", [5, 1, 8, 7, 2, 6, 4, 3]),
        ("Ordenado", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ("Invertido", [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]),
        ("Duplicados", [4, 1, 3, 4, 1, 2, 4, 3]),
        ("Todos Iguais", [5, 5, 5, 5, 5, 5, 5, 5]),
        ("Aleatório Médio", [3, 6, 2, 8, 4, 7, 5, 1, 9, 0]),
        ("Aleatório Grande", [90, 57, 99, 90, 54, 74, 55, 90, 7, 28, 21, 14, 79, 91, 20, 8, 94, 30, 7, 7])
    ]

    for name, data in test_cases:
        logging.info(f"Caso {name}: {data}")
        sorted_data, comparisons = multizip_sort(data[:])
        logging.info(f"Dados ordenados: {sorted_data}")
        logging.info(f"Número de comparações: {comparisons}")
        print(f"Caso {name} - Dados ordenados: {sorted_data}")
        print(f"Caso {name} - Número de comparações: {comparisons}")

    # Teste com limite de tempo
    for name, data in test_cases:
        logging.info(f"Caso {name} (Limite de tempo 0.01s): {data}")
        sorted_data, comparisons = multizip_sort(data[:], time_limit=0.01)
        logging.info(f"Dados ordenados (com limite de tempo): {sorted_data}")
        logging.info(f"Número de comparações (com limite de tempo): {comparisons}")
        print(f"Caso {name} (Limite de tempo 0.01s) - Dados ordenados: {sorted_data}")
        print(f"Caso {name} (Limite de tempo 0.01s) - Número de comparações: {comparisons}")
