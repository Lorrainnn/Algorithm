import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 读取CSV
csv_file = 'C:/Users/25181/Desktop/Algorithm/phase2/sorting_experiment_results.csv'

data = pd.read_csv(csv_file, header=None)
data.columns = ['Sort Algorithm', 'Distribution', 'Input Size', 'Average Time (seconds)']

# 确保输出文件夹存在
output_folder = "plots_combined_bestfit"
os.makedirs(output_folder, exist_ok=True)

# 获取所有算法
algorithms = data['Sort Algorithm'].unique()
distributions = data['Distribution'].unique()

# 画每个算法的三种输入组合图
def plot_log_log_combined(df, algorithm):
    plt.figure()

    for distribution in distributions:
        subset = df[(df['Sort Algorithm'] == algorithm) & (df['Distribution'] == distribution)]
        subset = subset.sort_values(by='Input Size')

        sizes = subset['Input Size'].values
        times = subset['Average Time (seconds)'].values

        log_sizes = np.log10(sizes)
        log_times = np.log10(times)

        # 拟合直线
        slope, intercept = np.polyfit(log_sizes, log_times, 1)
        predicted = slope * log_sizes + intercept

        # 计算R²值（拟合度）
        ss_res = np.sum((log_times - predicted) ** 2)
        ss_tot = np.sum((log_times - np.mean(log_times)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)

        # 画散点
        plt.scatter(log_sizes, log_times)

        # 画拟合线
        plt.plot(log_sizes, predicted, linestyle='--', label=f"{distribution}: {slope:.3f} log(x) + {intercept:.3f}, R²={r_squared:.3f}")

    plt.xlabel('log10(Input Size)')
    plt.ylabel('log10(Average Time (seconds))')
    plt.title(f'{algorithm} on Different Input Distributions')
    plt.legend()
    plt.grid(True)

    # 保存图片
    plot_filename = f"{output_folder}/{algorithm.replace(' ', '_')}_combined_bestfit.png"
    plt.savefig(plot_filename)
    plt.close()

    print(f"Saved combined plot with best fits: {plot_filename}")

# 主逻辑：每个算法一张图
for algorithm in algorithms:
    plot_log_log_combined(data, algorithm)

print("\nAll upgraded plots (with best fits) have been generated and saved!")
