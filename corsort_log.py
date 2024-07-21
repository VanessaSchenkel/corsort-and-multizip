import numpy as np
from loguru import logger

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

    def mark_elements(original, i, j):
        marked_list = []
        for idx, element in enumerate(original):
            if idx == i or idx == j:
                marked_list.append(f"({element})")
            else:
                marked_list.append(str(element))
        return marked_list

    delta, rho = compute_estimators(M)
    step = 1
    original_list = X.copy()

    while np.any(M == 0):
        try:
            I = delta + np.sum(M == 1, axis=0) + np.sum(M == 1, axis=1)
            i, j = choose_next_comparison(M, delta, I)
            logger.debug(f"Passo {step}: Comparando elementos {i} ({X[i]}) e {j} ({X[j]})")
            if not compare(X[i], X[j]):
                i, j = j, i
            M = update_partial_order(M, i, j)
            logger.debug(f"Passo {step}: Atualizado elementos {i} ({X[i]}) como menor que {j} ({X[j]})")
            delta, rho = compute_estimators(M)
            
            marked_partial_list = mark_elements(X, i, j)
            logger.info(f"Passo {step}: Lista parcialmente ordenada: {marked_partial_list}")
            step += 1
        except RuntimeError:
            logger.error("Número máximo de comparações atingido")
            break

    sorted_list = [x for _, x in sorted(zip(rho, X))]
    logger.info("Corsort concluído")
    return sorted_list

def main():
    data = [5, 3, 8, 2, 4, 7, 1, 9, 6]
    
    max_comparisons_list = [5, 10, 20]
    
    for max_comparisons in max_comparisons_list:
        logger.info(f"Executando Corsort com máximo de {max_comparisons} comparações")
        try:
            sorted_data, used_comparisons = corsort(data.copy(), max_comparisons=max_comparisons)
            logger.info(f"Dados ordenados: {sorted_data}")
            logger.info(f"Comparações usadas: {used_comparisons}")
        except RuntimeError as e:
            logger.error(str(e))

if __name__ == "__main__":
    main()
