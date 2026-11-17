import matplotlib.pyplot as plt
import numpy as np


threads = []
times = []
speedups = []
efficiencies = []

with open('scalability_data.txt', 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        data = line.split()
        threads.append(int(data[0]))
        times.append(float(data[1]))
        speedups.append(float(data[2]))
        efficiencies.append(float(data[3]))


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(threads, speedups, 'bo-', linewidth=2, markersize=8, label='Реальное ускорение')
ax1.plot(threads, threads, 'r--', linewidth=2, label='Идеальное ускорение')
ax1.set_xlabel('Число потоков', fontsize=12)
ax1.set_ylabel('Ускорение', fontsize=12)
ax1.set_title('Масштабируемость программы', fontsize=14)
ax1.legend()
ax1.grid(True, alpha=0.3)


ax2.plot(threads, efficiencies, 'go-', linewidth=2, markersize=8)
ax2.axhline(y=100, color='r', linestyle='--', linewidth=2, label='Идеальная эффективность')
ax2.set_xlabel('Число потоков', fontsize=12)
ax2.set_ylabel('Эффективность (%)', fontsize=12)
ax2.set_title('Эффективность параллелизации', fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('scalability_graph.png', dpi=300)
plt.show()


print("=" * 60)
print("СТАТИСТИКА МАСШТАБИРУЕМОСТИ")
print("=" * 60)
print(f"{'Потоки':<10} {'Время (с)':<15} {'Ускорение':<15} {'Эффективность':<15}")
print("-" * 60)
for i in range(len(threads)):
    print(f"{threads[i]:<10} {times[i]:<15.6f} {speedups[i]:<15.4f} {efficiencies[i]:<15.2f}%")