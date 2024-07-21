import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('results/performance_profiles_results.csv')

def normalize_times(df):
    normalized_df = df.copy()
    instance_groups = df.groupby('file')
    
    for name, group in instance_groups:
        min_times = group.loc[:, 'corsort_duration':'counting_sort_duration'].min(axis=1)
        for col in group.loc[:, 'corsort_duration':'counting_sort_duration']:
            normalized_df.loc[group.index, col] = group[col] / min_times.values
        
    return normalized_df

normalized_df = normalize_times(df)

def plot_combined_performance_profiles(normalized_df):
    algorithms = normalized_df.columns[2::2]  
    time_factors = [1, 2, 5, 10] 
    time_limits_labels = {0.001: '1ms', 0.01: '10ms', 0.1: '100ms', 1: '1s', 10: '10s'}
    
    plt.figure(figsize=(12, 8))

    for algo in algorithms:
        proportions = []
        for time_limit in normalized_df['time_limit'].unique():
            for time_factor in time_factors:
                proportion = (normalized_df[algo] <= time_factor * time_limit).mean()
                proportions.append(proportion)
        
        plt.plot([f"{time_limits_labels[tl]} (x{tf})" for tf in time_factors for tl in normalized_df['time_limit'].unique()], 
                 proportions, label=algo.split('_')[0])
    
    plt.xlabel('Time Limit')
    plt.ylabel('Proportion of Instances Solved')
    plt.title('Performance Profiles')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.savefig('images/combined_performance_profile.png')
    plt.show()

plot_combined_performance_profiles(normalized_df)
