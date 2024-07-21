import logging
import time
import os

logger = logging.getLogger(__name__)

def quick_sort(arr, time_limit=None):
    comparisons = 0
    start_time = time.time()

    def partition(arr, low, high):
        nonlocal comparisons
        i = low - 1
        pivot = arr[high]

        for j in range(low, high):
            comparisons += 1
            if arr[j] <= pivot:
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    size = len(arr)
    stack = [(0, size - 1)]

    while stack:
        if time_limit and (time.time() - start_time) > time_limit:
            logger.info("Tempo limite atingido, interrompendo Quick Sort")
            break
        low, high = stack.pop()
        if low < high:
            pi = partition(arr, low, high)
            stack.append((low, pi - 1))
            stack.append((pi + 1, high))

    return arr, comparisons

def load_list_from_file(file_path):
    """
    Carrega uma lista a partir de um arquivo.
    """
    with open(file_path, 'r') as f:
        return [int(item) for item in f.readline().strip().split(',')]

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    data_folder = 'data'
    file_paths = [os.path.join(data_folder, file) for file in os.listdir(data_folder) if file.endswith('.txt')]

    for file_path in file_paths:
        test_array = load_list_from_file(file_path)
        logger.info(f"--- Testando com arquivo: {file_path} ---")
        logger.info(f"Lista original: {test_array[:20]}... (mostrando os primeiros 20 elementos)")
        sorted_array, comparisons = quick_sort(test_array.copy(), time_limit=0.01)  # Defina o tempo limite aqui
        logger.info(f"Lista ordenada: {sorted_array[:20]}... (mostrando os primeiros 20 elementos)")
        logger.info(f"Número de comparações: {comparisons}")
        logger.info("\n")
    
    # Teste específico para o quick_sort com tempo limite
    logger.info("--- Teste específico para o Quick Sort com tempo limite ---")
    test_array = [3, 6, 8, 10, 1, 2, 1]
    logger.info(f"Lista original: {test_array}")
    sorted_array, comparisons = quick_sort(test_array.copy(), time_limit=0.0001)  # Tempo limite muito baixo para garantir interrupção
    logger.info(f"Lista ordenada: {sorted_array}")
    logger.info(f"Número de comparações: {comparisons}")
    logger.info("\n")
