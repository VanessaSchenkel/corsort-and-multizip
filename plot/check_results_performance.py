import json
import matplotlib.pyplot as plt
import numpy as np

def load_results(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def extract_conditions_and_sizes(results):
    conditions = set()
    sizes = set()
    for result in results:
        file_name = result['file']
        condition = '_'.join(file_name.split('_')[:-1])
        size = int(file_name.split('_')[-1].split('.')[0])
        conditions.add(condition)
        sizes.add(size)
    return sorted(conditions), sorted(sizes)

def generate_comparison_graphs(results):
    conditions, sizes = extract_conditions_and_sizes(results)
    
    for condition in conditions:
        condition_results = [r for r in results if condition in r['file']]
        
        time_limits = sorted(set(r['time_limit'] for r in condition_results))
        corsort_comparisons = {tl: [] for tl in time_limits}
        multizip_comparisons = {tl: [] for tl in time_limits}

        for r in condition_results:
            time_limit = r['time_limit']
            corsort_comparisons[time_limit].append(r['corsort']['comparisons'])
            multizip_comparisons[time_limit].append(r['multizip_sort']['comparisons'])

        corsort_means = [np.mean(corsort_comparisons[tl]) for tl in time_limits]
        multizip_means = [np.mean(multizip_comparisons[tl]) for tl in time_limits]

        plt.figure()
        plt.plot(time_limits, corsort_means, 'o-', label='Corsort')
        plt.plot(time_limits, multizip_means, 'x-', label='Multizip Sort')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Limite de Tempo (s)')
        plt.ylabel('Número de Comparações (Média)')
        plt.title(f'Comparação do Número de Comparações ({condition})')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'comparison_{condition}_comparisons_vs_time_limit.png')
        plt.close()
        
        corsort_durations = {tl: [] for tl in time_limits}
        multizip_durations = {tl: [] for tl in time_limits}

        for r in condition_results:
            time_limit = r['time_limit']
            corsort_durations[time_limit].append(r['corsort']['duration'])
            multizip_durations[time_limit].append(r['multizip_sort']['duration'])

        corsort_duration_means = [np.mean(corsort_durations[tl]) for tl in time_limits]
        multizip_duration_means = [np.mean(multizip_durations[tl]) for tl in time_limits]

        plt.figure()
        plt.plot(time_limits, corsort_duration_means, 'o-', label='Corsort')
        plt.plot(time_limits, multizip_duration_means, 'x-', label='Multizip Sort')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Limite de Tempo (s)')
        plt.ylabel('Tempo de Execução (s)')
        plt.title(f'Comparação do Tempo de Execução ({condition})')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'comparison_{condition}_duration_vs_time_limit.png')
        plt.close()

    for time_limit in time_limits:
        size_results = [r for r in results if r['time_limit'] == time_limit]
        corsort_comparisons = {size: [] for size in sizes}
        multizip_comparisons = {size: [] for size in sizes}

        for r in size_results:
            size = int(r['file'].split('_')[-1].split('.')[0])
            corsort_comparisons[size].append(r['corsort']['comparisons'])
            multizip_comparisons[size].append(r['multizip_sort']['comparisons'])

        corsort_means = [np.mean(corsort_comparisons[size]) for size in sizes]
        multizip_means = [np.mean(multizip_comparisons[size]) for size in sizes]

        plt.figure()
        plt.plot(sizes, corsort_means, 'o-', label='Corsort')
        plt.plot(sizes, multizip_means, 'x-', label='Multizip Sort')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Tamanho da Lista')
        plt.ylabel('Número de Comparações (Média)')
        plt.title(f'Comparação do Número de Comparações (Limite de Tempo: {time_limit}s)')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'comparison_comparisons_vs_size_{time_limit}s.png')
        plt.close()

if __name__ == "__main__":
    results = load_results('performance_profiles_results.json')
    generate_comparison_graphs(results)
