import os

import numpy as np
import matplotlib.pyplot as plt

IMG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       '..', 'latex_laboratory', 'images'))
os.makedirs(IMG_DIR, exist_ok=True)


def save_fig(name):
    plt.savefig(os.path.join(IMG_DIR, name), dpi=200, bbox_inches='tight')


def integrate(y, x):
    return np.sum((y[1:] + y[:-1]) / 2 * np.diff(x))


def rect(t, a, b):
    """Прямоугольный импульс единичной амплитуды на интервале [a, b]."""
    return np.where((t >= a) & (t <= b), 1.0, 0.0)


# =========================================================
# 1.1 Вычисление интеграла свертки аналитическим способом
# =========================================================
# s1(t) = 1 на [0, 1], s2(t) = 1 на [0, 2] (длительности 1 и 2 сек)
# y(t) = integral s2(u) * s1(t - u) du
# s1(t - u) = 1 при t-1 <= u <= t, поэтому пределы интегрирования:
#   max(0, t-1) <= u <= min(2, t)
# y(t) = min(2, t) - max(0, t-1) на пересечении, иначе 0:
#   t < 0:        y = 0
#   0 <= t < 1:   y = t            (нарастание)
#   1 <= t <= 2:  y = 1            (плато = меньшая длительность)
#   2 < t <= 3:   y = 3 - t        (спадание)
#   t > 3:        y = 0
print("=== 1.1 Аналитическое вычисление свертки ===")
for t_a in [-0.5, 0.5, 1.5, 2.5, 3.5]:
    lo = max(0.0, t_a - 1)
    hi = min(2.0, t_a)
    y_a = hi - lo if hi > lo else 0.0
    if hi <= lo:
        print(f"t = {t_a:5.2f}: пересечения нет -> y = 0")
    else:
        print(f"t = {t_a:5.2f}: пределы [{lo:.2f}, {hi:.2f}] -> y = {y_a:.2f}")

# =========================================================
# 1.2 Вычисление интеграла свертки численным интегрированием
# =========================================================
print("\n=== 1.2 Численная свертка двух прямоугольных импульсов ===")
tau = np.linspace(-5, 5, 10001)
s2_tau = rect(tau, 0, 2)

# График s1(-tau)
s1_minus_tau = rect(-tau, 0, 1)
plt.figure(figsize=(10, 4))
plt.plot(tau, s1_minus_tau, 'b')
plt.plot(tau, s2_tau, 'r', label='s2(τ)')
plt.plot(tau, s1_minus_tau, 'b', linestyle='--', label='s1(−τ)')
plt.title('Замена переменной: s1(−τ) и s2(τ)')
plt.xlabel('τ, сек')
plt.grid(True)
plt.legend()

# s1(t − τ) и произведения s2(τ)·s1(t−τ) для t = -1, 0, 2
save_fig('lab5_fig1_s1_minus_tau.png')
t_list = [-1, 0, 2]
plt.figure(figsize=(12, 8))
for i, t_val in enumerate(t_list):
    s1_shift = rect(tau, t_val - 1, t_val)
    prod = s2_tau * s1_shift
    plt.subplot(3, 2, 2 * i + 1)
    plt.plot(tau, s2_tau, 'r', label='s2(τ)')
    plt.plot(tau, s1_shift, 'b', linestyle='--', label=f's1({t_val}−τ)')
    plt.grid(True)
    plt.legend()
    plt.xlabel('τ')
    plt.subplot(3, 2, 2 * i + 2)
    plt.plot(tau, prod, 'g')
    plt.title(f'Произведение s2(τ)·s1({t_val}−τ), integral = {integrate(prod, tau):.3f}')
    plt.grid(True)
    plt.xlabel('τ')
plt.tight_layout()

# Интеграл свертки для t = 0, 0.2, 1
print("Интегралы для отдельных моментов t:")
for t_val in [0, 0.2, 1]:
    prod = s2_tau * rect(tau, t_val - 1, t_val)
    print(f"  t = {t_val:4.2f}: y(t) = {integrate(prod, tau):.3f}")

# Интеграл для каждого t на (-1, 4) с шагом 0.05
t_sweep = np.arange(-1, 4.001, 0.05)
y_num = np.array([integrate(s2_tau * rect(tau, tv - 1, tv), tau) for tv in t_sweep])

# Трапеция (аналитический результат) для сравнения
y_an = np.clip(t_sweep, 0, None)
y_an = np.where((t_sweep >= 0) & (t_sweep < 1), t_sweep, y_an)
y_an = np.where((t_sweep >= 1) & (t_sweep <= 2), 1.0, y_an)
y_an = np.where((t_sweep > 2) & (t_sweep <= 3), 3 - t_sweep, y_an)
y_an = np.where(t_sweep > 3, 0.0, y_an)

print(f"Макс. отклонение числ. свертки от аналитической: "
      f"{np.max(np.abs(y_num - y_an)):.4f}")

save_fig('lab5_fig2_products.png')
plt.figure(figsize=(10, 5))
plt.plot(t_sweep, y_num, 'o-', label='Численная свертка')
plt.plot(t_sweep, y_an, 'r--', linewidth=2, label='Аналитическая трапеция')
plt.title('Свертка прямоугольных импульсов (τ=1 и τ=2): трапецеидальный импульс')
plt.xlabel('t, сек')
plt.ylabel('y(t)')
plt.grid(True)
plt.legend()

# =========================================================
# 1.3 Свертка прямоугольного сигнала и гармонического колебания
# =========================================================
print("\n=== 1.3 Свертка импульса и гармонического колебания ===")
f_h = 0.5  # колебание длительностью 4 сек = 2 периода
s2_harm = np.where((tau >= 0) & (tau <= 4), np.cos(2 * np.pi * f_h * tau), 0.0)

t_sweep2 = np.arange(-1, 8.001, 0.05)
y_harm = np.array([integrate(s2_harm * rect(tau, tv - 1, tv), tau) for tv in t_sweep2])

save_fig('lab5_fig3_convolution_rects.png')
plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
plt.plot(tau, s2_harm, 'r', label='s2(t) — косинус, 4 сек')
plt.plot(tau, rect(tau, 0, 1) - 0.3, 'b', linestyle='--', label='s1(t) — импульс 1 сек')
plt.title('Исходные сигналы')
plt.xlabel('t, сек')
plt.grid(True)
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(t_sweep2, y_harm, 'g')
plt.title('Результат свертки y(t)')
plt.xlabel('t, сек')
plt.ylabel('y(t)')
plt.grid(True)
plt.tight_layout()

# =========================================================
# 1.4 Связь свертки и преобразования Фурье
# =========================================================
print("\n=== 1.4 Связь свертки и ПФ ===")
t_ft = np.linspace(-5, 7, 12000)
s1_t = rect(t_ft, 0, 1)
s2_t = rect(t_ft, 0, 2)

# y(t) на мелкой сетке для точного ПФ
t_fine = np.linspace(-1, 4, 1001)
y_t = np.array([integrate(s2_tau * rect(tau, tv - 1, tv), tau) for tv in t_fine])

f = np.linspace(-3, 3, 400)
S1 = np.array([integrate(s1_t * np.exp(-1j * 2 * np.pi * fv * t_ft), t_ft) for fv in f])
S2 = np.array([integrate(s2_t * np.exp(-1j * 2 * np.pi * fv * t_ft), t_ft) for fv in f])
SY = np.array([integrate(y_t * np.exp(-1j * 2 * np.pi * fv * t_fine), t_fine) for fv in f])

prod = S1 * S2
err = np.max(np.abs(SY - prod))
rel = np.max(np.abs(SY[10:-10] - prod[10:-10])) / np.max(np.abs(prod[10:-10]))
print(f"Сравнение ПФ свертки Y(jω) и произведения S1(jω)·S2(jω):")
print(f"  макс. абсолютная погрешность: {err:.5f}")
print(f"  макс. относительная погрешность (в зоне значимых значений): {rel * 100:.2f} %")
print("  Вывод: спектр свертки равен произведению спектров — свойство подтверждено.")

save_fig('lab5_fig4_rect_cos.png')
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(f, np.abs(SY), 'b', linewidth=2, label='|ПФ свертки|')
plt.plot(f, np.abs(prod), 'r--', label='|S1(jω)·S2(jω)|')
plt.title('Связь свертки и преобразования Фурье')
plt.xlabel('Частота f, Гц')
plt.ylabel('Модуль')
plt.grid(True)
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(f, np.angle(SY), 'b', label='arg ПФ свертки')
plt.plot(f, np.angle(prod), 'r--', label='arg S1·S2')
plt.xlabel('Частота f, Гц')
plt.ylabel('Аргумент, рад')
plt.grid(True)
plt.legend()
plt.tight_layout()

save_fig('lab5_fig5_ft_property.png')
plt.show()
