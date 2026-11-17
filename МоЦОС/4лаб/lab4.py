import numpy as np
import matplotlib.pyplot as plt

def integrate(y, x):
    return np.sum((y[1:] + y[:-1]) / 2 * np.diff(x))

tau = 2.0
fc = 3.0
t = np.linspace(-5, 10, 8000)
f = np.linspace(-6, 6, 1200)

x_rect = np.where((t >= 0) & (t <= tau), 1.0, 0.0)
x_cos = np.cos(2 * np.pi * fc * t)
x_mod = x_rect * x_cos

X_rect = np.zeros(len(f), dtype=complex)
X_mod = np.zeros(len(f), dtype=complex)
for i, freq in enumerate(f):
    X_rect[i] = integrate(x_rect * np.exp(-1j * 2 * np.pi * freq * t), t)
    X_mod[i] = integrate(x_mod * np.exp(-1j * 2 * np.pi * freq * t), t)

plt.figure(figsize=(12, 8))
plt.subplot(3, 1, 1)
plt.plot(t, x_rect, 'b', label='Прямоугольный импульс')
plt.plot(t, x_mod, 'r', label='Модулированный сигнал')
plt.title('Сигналы во времени')
plt.xlabel('Время t, сек')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.legend()
plt.ylim(-1.5, 1.5)

plt.subplot(3, 1, 2)
plt.plot(f, np.abs(X_rect), 'b', label='Спектр импульса')
plt.title('Модуль спектра исходного прямоугольного импульса')
plt.xlabel('Частота f, Гц')
plt.ylabel('|X(f)|')
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(f, np.abs(X_mod), 'r', label='Спектр модулированного сигнала')
plt.axvline(fc, color='g', linestyle='--', label=f'f_c = {fc} Гц')
plt.axvline(-fc, color='g', linestyle='--')
plt.title('Модуль спектра после модуляции (сдвиг на ±f_c)')
plt.xlabel('Частота f, Гц')
plt.ylabel('|X(f)|')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()