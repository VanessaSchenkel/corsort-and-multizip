import os
import numpy as np

def generate_list(size, list_type):
    if list_type == 'random':
        return np.random.permutation(size).tolist()
    elif list_type == 'sorted':
        return list(range(size))
    elif list_type == 'reversed':
        return list(range(size, 0, -1))
    elif list_type == 'nearly_sorted':
        arr = list(range(size))
        for _ in range(size // 10): 
            i = np.random.randint(size)
            j = np.random.randint(size)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    elif list_type == 'many_duplicates':
        num_unique_elements = max(1, size // 10)  # Garante pelo menos 1 elemento único
        return np.random.choice(range(num_unique_elements), size).tolist()  # Apenas 10% de valores únicos
    else:
        raise ValueError("Tipo de lista não suportado")

# Tamanhos das listas conforme o artigo
list_sizes = [8, 16, 32, 64, 128, 256, 512, 1024, 2048]
list_types = ['random', 'sorted', 'reversed', 'nearly_sorted', 'many_duplicates']

output_dir = 'data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for size in list_sizes:
    for list_type in list_types:
        generated_list = generate_list(size, list_type)
        file_path = os.path.join(output_dir, f'list_{list_type}_{size}.txt')
        with open(file_path, 'w') as file:
            file.write(','.join(map(str, generated_list)))

print("Listas geradas e salvas na pasta 'data'.")
