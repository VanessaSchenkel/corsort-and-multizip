import sys
import os
import random
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from loguru import logger
import numpy as np

def count_comparisons(compare_fn):
    """
    Decorator to count the number of comparisons made by a sorting algorithm.
    """
    def wrapper(X, *args, **kwargs):
        wrapper.count = 0
        def compare(a, b):
            wrapper.count += 1
            return a < b
        result = compare_fn(X, compare=compare, *args, **kwargs)
        return result, wrapper.count
    return wrapper

@count_comparisons
def corsort(X, compare, time_limit=None):
    logger.info("Iniciando Corsort")
    start_time = time.time()
    n = len(X)
    M = np.eye(n)

    def update_partial_order(M, i, j):
        # logger.debug(f"Atualizando ordem parcial para comparação ({i}, {j})")
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
        if time_limit and (time.time() - start_time) > time_limit:
            logger.info("Tempo limite atingido, interrompendo Corsort")
            break
        I = delta + np.sum(M == 1, axis=0) + np.sum(M == 1, axis=1)
        i, j = choose_next_comparison(M, delta, I)
        if not compare(X[i], X[j]):
            i, j = j, i
        M = update_partial_order(M, i, j)
        delta, rho = compute_estimators(M)
    sorted_list = [x for _, x in sorted(zip(rho, X))]
    logger.info("Corsort concluído")
    return sorted_list

if __name__ == "__main__":
    logger.add("logs/app.log")
    
    # Cenários de teste
    test_cases = {
        "Caso 1 - Aleatório Pequeno": [5, 1, 8, 7, 2, 6, 4, 3],
        "Caso 2 - Ordenado": list(range(10)),
        "Caso 3 - Invertido": list(range(10, 0, -1)),
        "Caso 4 - Duplicados": [4, 1, 3, 4, 1, 2, 4, 3],
        "Caso 5 - Todos Iguais": [5, 5, 5, 5, 5, 5, 5, 5],
        "Caso 6 - Aleatório Médio": [3, 6, 2, 8, 4, 7, 5, 1, 9, 0],
        "Caso 7 - Aleatório Grande": [random.randint(0, 100) for _ in range(20)]
    }

    # Testes sem limite de tempo
    for description, sample_data in test_cases.items():
        logger.info(f"{description} (Sem limite de tempo): {sample_data}")
        sorted_data, num_comparisons = corsort(sample_data)
        logger.info(f"Dados ordenados: {sorted_data}")
        logger.info(f"Número de comparações: {num_comparisons}")
        print(f"{description} - Dados ordenados: {sorted_data}")
        print(f"{description} - Número de comparações: {num_comparisons}")

    # Testes com limite de tempo muito curto
    time_limit = 0.01  # 10 ms
    for description, sample_data in test_cases.items():
        logger.info(f"{description} (Limite de tempo {time_limit}s): {sample_data}")
        sorted_data, num_comparisons = corsort(sample_data, time_limit=time_limit)
        logger.info(f"Dados ordenados (com limite de tempo): {sorted_data}")
        logger.info(f"Número de comparações (com limite de tempo): {num_comparisons}")
        print(f"{description} (Limite de tempo {time_limit}s) - Dados ordenados: {sorted_data}")
        print(f"{description} (Limite de tempo {time_limit}s) - Número de comparações: {num_comparisons}")
