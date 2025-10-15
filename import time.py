import time
import random
import numpy as np
import matplotlib.pyplot as plt

# ==========================
# Base Class: Algorithm
# ==========================
class Algorithm:
    def __init__(self, name):
        self.name = name

    def run(self, data):
        raise NotImplementedError("Subclasses must override run()")

# ==========================
# CPU Simulation Class
# ==========================
class PipelineCPU:
    def __init__(self, name="Basic", stages=1):
        self.name = name
        self.stages = stages

    def process_delay(self):
        """
        Simulate pipeline delay:
        - More stages => smaller delay (faster execution)
        - No pipeline => higher delay
        """
        base_delay = 0.00002
        delay = base_delay / self.stages
        time.sleep(delay)

# ==========================
# Quick Sort Algorithm
# ==========================
class QuickSort(Algorithm):
    def __init__(self, cpu):
        super().__init__("Quick Sort")
        self.cpu = cpu

    def partition(self, arr, low, high):
        i = low - 1
        pivot = arr[high]
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
            # simulate pipeline delay for each comparison
            self.cpu.process_delay()
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quick_sort(self, arr, low, high):
        if low < high:
            pi = self.partition(arr, low, high)
            self.quick_sort(arr, low, pi - 1)
            self.quick_sort(arr, pi + 1, high)

    def run(self, data):
        arr_copy = data.copy()
        start = time.time()
        self.quick_sort(arr_copy, 0, len(arr_copy) - 1)
        end = time.time()
        return end - start

# ==========================
# Performance Analyzer
# ==========================
class PerformanceAnalyzer:
    def __init__(self, algorithm, runs=5, input_size=1000):
        self.algorithm = algorithm
        self.runs = runs
        self.input_size = input_size
        self.times = []

    def execute(self):
        for i in range(self.runs):
            data = [random.randint(1, 10000) for _ in range(self.input_size)]
            t = self.algorithm.run(data)
            self.times.append(t)
        return self.times

    def statistics(self):
        mean_time = np.mean(self.times)
        variance_time = np.var(self.times)
        std_dev = np.std(self.times)
        return mean_time, variance_time, std_dev

# ==========================
# Main Function
# ==========================
def main():
    input_size = 1000
    runs = 5

    # Define different CPU pipeline configurations
    cpu_configs = [
        PipelineCPU("Basic (No Pipeline)", stages=1),
        PipelineCPU("2-Stage Pipeline", stages=2),
        PipelineCPU("4-Stage Pipeline", stages=4)
    ]

    results = []

    for cpu in cpu_configs:
        algo = QuickSort(cpu)
        analyzer = PerformanceAnalyzer(algo, runs, input_size)
        analyzer.execute()
        mean_time, variance_time, std_dev = analyzer.statistics()

        print(f"\nCPU: {cpu.name}")
        print(f"Mean Time: {mean_time:.5f}s")
        print(f"Variance: {variance_time:.8f}")
        print(f"Std Deviation: {std_dev:.5f}")

        results.append((cpu.name, mean_time, variance_time, std_dev))

    # ==========================
    # Visualization
    # ==========================
    labels = [r[0] for r in results]
    means = [r[1] for r in results]

    plt.bar(labels, means, color='skyblue')
    plt.xlabel("CPU Type")
    plt.ylabel("Mean Execution Time (s)")
    plt.title("Quick Sort Performance under Different Pipeline Stages")
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

    # ==========================
    # Summary Table
    # ==========================
    print("\nPerformance Summary:")
    print(f"{'CPU Type':<20}{'Mean (s)':<15}{'Variance':<15}{'Std Dev':<15}")
    print("-" * 65)
    for r in results:
        print(f"{r[0]:<20}{r[1]:<15.5f}{r[2]:<15.8f}{r[3]:<15.5f}")

if __name__ == "__main__":
    main()
