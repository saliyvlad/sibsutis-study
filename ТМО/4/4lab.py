# ИКС-431 Салий Владислав, доп. задание 1 (Python)
# Моделирование цепи Маркова (Вариант 18)

import numpy as np
import matplotlib.pyplot as plt

# 1. Исходная матрица коэффициентов варианта 18
P_raw = np.array([
    [5, 5, 1, 0],
    [5, 5, 2, 0],
    [2, 5, 5, 2],
    [0, 0, 3, 3]
], dtype=float)

# Нормировка по строкам (получаем стохастическую матрицу)
P = P_raw / P_raw.sum(axis=1, keepdims=True)

print("Исходная матрица коэффициентов:")
print(P_raw.astype(int))
print("\nНормированная матрица переходов P:")
print(np.round(P, 4))
print("\nСуммы по строкам (должны быть = 1):", P.sum(axis=1))

# Состояния
states = ['Healthy', 'Unwell', 'Sick', 'Very sick']

# Кумулятивная матрица для моделирования
P_cum = np.cumsum(P, axis=1)
print("\nКумулятивная матрица P_cum:")
print(np.round(P_cum, 4))

# 2. Функция моделирования траектории (ИСПРАВЛЕНА)
def simulate_chain(P_cum, T, start=0):
    """Моделирование траектории цепи Маркова."""
    z = np.zeros(T, dtype=int)
    z[0] = start
    n_states = P_cum.shape[0]  # Количество состояний
    
    for t in range(T - 1):
        r = np.random.rand()
        # Находим следующее состояние
        next_state = np.sum(r > P_cum[z[t]])
        # Ограничиваем диапазоном [0, n_states-1]
        next_state = min(next_state, n_states - 1)
        z[t + 1] = next_state
    
    return z

# 3. Функция оценки матрицы переходов по траектории
def estimate_P(z, n_states):
    """Оценка матрицы переходов по траектории."""
    P_obs = np.zeros((n_states, n_states))
    for t in range(len(z) - 1):
        P_obs[z[t], z[t + 1]] += 1
    row_sums = P_obs.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1  # защита от деления на 0
    return P_obs / row_sums

# 4. Моделирование для разных T
iterations = [200, 1000, 10000]
fig, axes = plt.subplots(3, 1, figsize=(12, 9))

for idx, T in enumerate(iterations):
    z = simulate_chain(P_cum, T, start=0)
    P_obs = estimate_P(z, 4)
    
    axes[idx].plot(z, linewidth=0.8, color='steelblue')
    axes[idx].set_title(f'Траектория цепи Маркова (T={T})')
    axes[idx].set_xlabel('Итерация')
    axes[idx].set_ylabel('Состояние')
    axes[idx].set_yticks([0, 1, 2, 3])
    axes[idx].set_yticklabels(states)
    axes[idx].grid(True, alpha=0.3)
    axes[idx].set_ylim(-0.5, 3.5)
    
    print(f"\n--- Оценённая матрица для T={T} ---")
    print(np.round(P_obs, 4))

plt.tight_layout()
plt.savefig('lab4_python_trajectories.png', dpi=150)
plt.show()

# 5. Сравнение двух траекторий T=200
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
for i, ax in enumerate(axes):
    z = simulate_chain(P_cum, 200, start=0)
    ax.plot(z, linewidth=0.8, color='crimson' if i else 'steelblue')
    ax.set_title(f'Траектория {i+1} (T=200)')
    ax.set_xlabel('Итерация')
    ax.set_ylabel('Состояние')
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(states)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.5, 3.5)

plt.suptitle('Сравнение двух независимых траекторий')
plt.tight_layout()
plt.savefig('lab4_python_compare.png', dpi=150)
plt.show()

print("\n=== Дополнительное задание 1 (Python) завершено ===")