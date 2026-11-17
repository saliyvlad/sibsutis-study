# import numpy as np
# import matplotlib.pyplot as plt

# A = 4
# w = 0.4 * np.pi
# phi = 0.25 * np.pi

# f = w / (2 * np.pi)
# T = 1 / f
# t_shift = -phi / w

# print(f"Уравнение: x(t) = {A}cos({w/np.pi:.2f}πt + {phi/np.pi:.2f}π)")
# print(f"Период T = {T:.2f} сек")
# print(f"Временной сдвиг максимума = {t_shift:.3f} сек")

# t = np.linspace(0, 3 * T, 1000)
# x = A * np.cos(w * t + phi)
# x_zero_phi = A * np.cos(w * t)

# plt.figure(figsize=(10, 5))
# plt.plot(t, x, label=f'x(t) с фазой {phi/np.pi:.2f}π', color='b')
# plt.plot(t, x_zero_phi, label='x(t) с нулевой фазой', color='r', linestyle='--')
# plt.title('Гармоническое колебание (2-3 периода)')
# plt.xlabel('Время t, сек')
# plt.ylabel('Амплитуда')
# plt.grid(True)
# plt.legend()
# plt.show()

import numpy as np
import matplotlib.pyplot as plt

# A = 4
# w = 0.4 * np.pi
# phi = 0.25 * np.pi

# f = w / (2 * np.pi)
# T = 1 / f
# t_shift = -phi / w

# print(f"Период T = {T:.2f} сек")
# print(f"Временной сдвиг максимума = {t_shift:.3f} сек")

# t = np.linspace(0, 3 * T, 1000)
# x = A * np.cos(w * t + phi)
# x_zero_phi = A * np.cos(w * t)

# plt.figure(figsize=(10, 5))
# plt.plot(t, x, label='x(t) с фазой 0.25π', color='b')
# plt.plot(t, x_zero_phi, label='x(t) с нулевой фазой', color='r', linestyle='--')
# plt.title('Гармоническое колебание (2-3 периода)')
# plt.xlabel('Время t, сек')
# plt.ylabel('Амплитуда')
# plt.grid(True)
# plt.legend()
# plt.show()

# T2 = 4.0
# w2 = 2 * np.pi / T2
# t_vals = np.array([-1, 3, 7])
# phases = w2 * t_vals + 0

# print(f"Период T = {T2} сек, частота f = {1/T2} Гц")
# for t_val, phase in zip(t_vals, phases):
#     print(f"Фаза в момент t = {t_val} сек: {phase/np.pi:.2f}π рад ({phase:.2f} рад)")

# a, b = 3, 4
# z1 = complex(a, b)
# z2 = complex(a, -b)

# r1, theta1 = np.abs(z1), np.angle(z1)
# r2, theta2 = np.abs(z2), np.angle(z2)

# print(f"z1 = {z1} -> Полярная форма: r={r1:.2f}, θ={theta1/np.pi:.3f}π ({np.degrees(theta1):.2f}°)")
# print(f"z2 = {z2} -> Полярная форма: r={r2:.2f}, θ={theta2/np.pi:.3f}π ({np.degrees(theta2):.2f}°)")

r_polar = 5.0
theta_polar = np.pi / 4
z_polar = r_polar * np.exp(1j * theta_polar)
print(f"Число из полярной формы (r={r_polar}, θ=π/4) -> Обычная форма: {z_polar.real:.2f} + {z_polar.imag:.2f}j")