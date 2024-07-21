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
                marked_partial_list = mark_elements(result, arr1[i - 1] if i > 0 else None, arr2[j - 1] if j > 0 else None)
                logger.info(f"Lista parcialmente ordenada no merge: {marked_partial_list}")
            except RuntimeError:
                logger.error("Número máximo de comparações atingido no merge")
                result.extend(arr1[i:])
                result.extend(arr2[j:])
                raise
        result.extend(arr1[i:])
        result.extend(arr2[j:])
        return result

    def mark_elements(original, i, j):
        marked_list = []
        for element in original:
            if element == i or element == j:
                marked_list.append(f"({element})")
            else:
                marked_list.append(str(element))
        return marked_list

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

def main():
    data = [5, 3, 8, 2, 4, 7, 1, 9, 6]
    
    max_comparisons_list = [5, 10, 20]
    
    for max_comparisons in max_comparisons_list:
        logger.info(f"Executando Multizip Sort com máximo de {max_comparisons} comparações")
        try:
            sorted_data, used_comparisons = multizip_sort(data.copy(), max_comparisons=max_comparisons)
            logger.info(f"Dados ordenados: {sorted_data}")
            logger.info(f"Comparações usadas: {used_comparisons}")
        except RuntimeError as e:
            logger.error(str(e))

if __name__ == "__main__":
    main()
