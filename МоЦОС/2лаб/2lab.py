# import numpy as np
# import matplotlib.pyplot as plt

# t = np.linspace(0, 1, 1000)
# A = 1
# f = 5
# phi_deg = [0, 90, 180, 270]

# plt.figure(figsize=(10, 8))
# for i in range(len(phi_deg)):
#     phi_rad = phi_deg[i] * np.pi / 180
#     x = A * np.sin(2 * np.pi * f * t + phi_rad)
#     plt.subplot(2, 2, i + 1)
#     plt.plot(t, x, color='purple')
#     plt.xlabel('Время(t)')
#     plt.ylabel('Амплитуда(V)')
#     plt.title(f'$\Phi = {phi_deg[i]}^\circ$')
#     plt.grid(True)
# plt.tight_layout()
# plt.show()

# f0 = 2
# w0 = 2 * np.pi * f0
# t3 = np.linspace(0, 2, 1000)

# A1, phi1 = 3, np.pi / 6
# A2, phi2 = 4, np.pi / 3
# x1 = A1 * np.cos(w0 * t3 + phi1)
# x2 = A2 * np.cos(w0 * t3 + phi2)
# x_sum2 = x1 + x2

# A3, phi3 = 2, -np.pi / 4
# x3 = A3 * np.cos(w0 * t3 + phi3)
# x_sum3 = x1 + x2 + x3

# plt.figure(figsize=(10, 6))
# plt.plot(t3, x1, '--', label='x1')
# plt.plot(t3, x2, '--', label='x2')
# plt.plot(t3, x_sum2, 'b', linewidth=2, label='Сумма 2-х')
# plt.plot(t3, x_sum3, 'r', linewidth=2, label='Сумма 3-х')
# plt.title('Сложение гармонических колебаний (N=2 и N=3)')
# plt.xlabel('Время, сек')
# plt.ylabel('Амплитуда')
# plt.legend()
# plt.grid(True)
# plt.show()

# f_base = 1
# t4 = np.linspace(0, 5, 5000)

# x_eq4 = (4 / np.pi) * np.cos(2 * np.pi * f_base * t4 - np.pi / 2) + \
#         (4 / (3 * np.pi)) * np.cos(2 * np.pi * 3 * f_base * t4 - np.pi / 2)

# N_harmonics = 5
# x_eq5 = np.zeros_like(t4)
# for n in range(1, N_harmonics + 1):
#     k = 2 * n - 1
#     x_eq5 += (4 / (k * np.pi)) * np.cos(2 * np.pi * k * f_base * t4 - np.pi / 2)

# plt.figure(figsize=(10, 6))
# plt.plot(t4, x_eq4, label='Уравнение 4 (2 гармоники)', color='orange')
# plt.plot(t4, x_eq5, label=f'Уравнение 5 ({N_harmonics} нечетных гармоник)', color='green')
# plt.title('Синтез периодического сигнала (ряд Фурье)')
# plt.xlabel('Время, сек')
# plt.ylabel('Амплитуда')
# plt.legend()
# plt.grid(True)
# plt.show()



# import numpy as np
# import matplotlib.pyplot as plt

# t = np.linspace(0, 1, 1000)
# A = 5
# f = 5
# ph = 0

# x = A * np.sin(2 * np.pi * f * t + ph)
# plt.plot(t, x)
# plt.xlabel('Time')
# plt.ylabel('Amplitude')
# plt.title('A={}V, F={}Hz, $\\phi={}^\\circ$'.format(A, f, ph))
# plt.show()

# import numpy as np
# import matplotlib.pyplot as plt

# t = np.linspace(0, 1, 100)
# A = 1
# f = 5
# phi = [0, 90, 180, 270]

# for i in range(len(phi)):
#     x = A * np.sin(2 * np.pi * f * t + phi[i] * np.pi / 180)
#     plt.subplot(2, 2, i + 1)
#     plt.plot(t, x)
#     plt.xlabel('Time(t)')
#     plt.ylabel('Amplitude(V)')
#     plt.title('$\\Phi={}^\\circ$'.format(phi[i]))
# plt.tight_layout()
# plt.show()

# import numpy as np
# import matplotlib.pyplot as plt

# t = np.linspace(0, 1, 1000)
# A1 = 3
# A2 = 4
# f = 2
# phi1 = 30
# phi2 = 60

# x1 = A1 * np.cos(2 * np.pi * f * t + phi1 * np.pi / 180)
# x2 = A2 * np.cos(2 * np.pi * f * t + phi2 * np.pi / 180)
# x_sum = x1 + x2

# plt.plot(t, x1, '--', label='x1')
# plt.plot(t, x2, '--', label='x2')
# plt.plot(t, x_sum, 'b', linewidth=2, label='Сумма')
# plt.xlabel('Время')
# plt.ylabel('Амплитуда')
# plt.title('Сложение 2 колебаний')
# plt.legend()
# plt.grid(True)
# plt.show()

# # Определение параметров суммарного колебания
# A_sum = np.max(x_sum)
# print(f"Амплитуда суммарного колебания: {A_sum:.2f}")

# import numpy as np
# import matplotlib.pyplot as plt

# t = np.linspace(0, 1, 1000)
# A1 = 3
# A2 = 4
# A3 = 2
# f = 2
# phi1 = 30
# phi2 = 60
# phi3 = -45

# x1 = A1 * np.cos(2 * np.pi * f * t + phi1 * np.pi / 180)
# x2 = A2 * np.cos(2 * np.pi * f * t + phi2 * np.pi / 180)
# x3 = A3 * np.cos(2 * np.pi * f * t + phi3 * np.pi / 180)
# x_sum = x1 + x2 + x3

# plt.plot(t, x1, '--', label='x1')
# plt.plot(t, x2, '--', label='x2')
# plt.plot(t, x3, '--', label='x3')
# plt.plot(t, x_sum, 'r', linewidth=2, label='Сумма 3-х')
# plt.xlabel('Time(t)')
# plt.ylabel('Amplitude(V)')
# plt.title('Сложение 3 колебаний')
# plt.legend()
# plt.grid(True)
# plt.show()

# A_sum = np.max(x_sum)
# print(f"Амплитуда суммарного колебания: {A_sum:.2f}")

# import numpy as np
# import matplotlib.pyplot as plt

# f = 1
# t = np.linspace(0, 5, 5000)

# x = (4 / np.pi) * np.cos(2 * np.pi * f * t - np.pi / 2) + \
#     (4 / (3 * np.pi)) * np.cos(2 * np.pi * 3 * f * t - np.pi / 2)

# plt.plot(t, x, color='orange')
# plt.xlabel('Время')
# plt.ylabel('Амплитуда')
# plt.title('Сложение колебаний с различными частотами (2 гармоники)')
# plt.grid(True)
# plt.show()

# import numpy as np
# import matplotlib.pyplot as plt

# f = 1
# t = np.linspace(0, 5, 5000)

# N_max = 5
# for N in [1, 3, 5]:
#     x = np.zeros_like(t)
#     for n in range(1, N + 1):
#         k = 2 * n - 1
#         x += (4 / (k * np.pi)) * np.cos(2 * np.pi * k * f * t - np.pi / 2)
    
#     plt.plot(t, x, label=f'N={N} гармоник')

# plt.xlabel('Время')
# plt.ylabel('Амплитуда')
# plt.title('Синтез сигнала рядом Фурье')
# plt.legend()
# plt.grid(True)
# plt.show()

import numpy as np
import matplotlib.pyplot as plt

t_exp = np.linspace(0, 2.5, 250)
f_exp = np.exp(2j * np.pi * 1 * t_exp)

fig = plt.figure(figsize=(8, 8))
ax = plt.axes(projection='3d')
ax.grid()
ax.plot3D(t_exp, f_exp.real, f_exp.imag, 'r')
ax.set_title('Комплексная экспонента')
ax.plot3D(t_exp, f_exp.real, np.zeros(250), 'b')
ax.plot3D(t_exp, np.zeros(250), f_exp.imag, 'g')
ax.set_xlabel('Time')
ax.set_ylabel('Real Axis')
ax.set_zlabel('Imag Axis')
plt.show()