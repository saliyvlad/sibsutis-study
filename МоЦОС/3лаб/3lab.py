import numpy as np
import matplotlib.pyplot as plt

def integrate(y, x):
    return np.sum((y[1:] + y[:-1]) / 2 * np.diff(x))

A_sig = 5
f_sig = 2
T_sig = 1 / f_sig
phi_sig = np.pi / 4

t1 = np.linspace(0, T_sig, 10000)
x_sig = A_sig * np.cos(2 * np.pi * f_sig * t1 + phi_sig)

n_vals = np.arange(0, 6)
a_n = []
b_n = []

for n in n_vals:
    cos_n = np.cos(2 * np.pi * n * f_sig * t1)
    sin_n = np.sin(2 * np.pi * n * f_sig * t1)
    
    coef = 1 / T_sig if n == 0 else 2 / T_sig 
    
    a_n.append(coef * integrate(x_sig * cos_n, t1))
    b_n.append(coef * integrate(x_sig * sin_n, t1))

a_n = np.array(a_n)
b_n = np.array(b_n)
A_n = np.sqrt(a_n**2 + b_n**2)
phi_n = np.arctan2(-b_n, a_n)

print(f"Коэффициенты An: {np.round(A_n, 3)}")
print(f"Коэффициенты phi_n (рад): {np.round(phi_n, 3)}")

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.stem(n_vals, A_n, basefmt=" ")
plt.title('Спектр амплитуд An')
plt.xlabel('n')
plt.ylabel('An')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.stem(n_vals, phi_n, basefmt=" ")
plt.title('Спектр фаз φn')
plt.xlabel('n')
plt.ylabel('φn, рад')
plt.grid(True)
plt.tight_layout()
plt.show()

T_rect = 1.0
tau = 0.25
f_rect = 1 / T_rect
t2 = np.linspace(0, 3 * T_rect, 3000)

x_rect = np.zeros_like(t2)
for i in range(len(t2)):
    if (t2[i] % T_rect) < tau:
        x_rect[i] = 1.0

N_max = 12
a_rect = []
b_rect = []
for n in range(N_max + 1):
    cos_n = np.cos(2 * np.pi * n * f_rect * t2)
    sin_n = np.sin(2 * np.pi * n * f_rect * t2)
    coef = 1 / T_rect if n == 0 else 2 / T_rect
    a_rect.append(coef * integrate(x_rect * cos_n, t2))
    b_rect.append(coef * integrate(x_rect * sin_n, t2))

a_rect = np.array(a_rect)
b_rect = np.array(b_rect)
A_rect = np.sqrt(a_rect**2 + b_rect**2)
phi_rect = np.arctan2(-b_rect, a_rect)

t_synth = np.linspace(0, 2 * T_rect, 2000)
x_synth_2 = np.zeros_like(t_synth)
x_synth_4 = np.zeros_like(t_synth)
x_synth_6 = np.zeros_like(t_synth)

for n in range(1, 7):
    harm = a_rect[n] * np.cos(2 * np.pi * n * f_rect * t_synth) + \
           b_rect[n] * np.sin(2 * np.pi * n * f_rect * t_synth)
    if n <= 2: x_synth_2 += harm
    if n <= 4: x_synth_4 += harm
    x_synth_6 += harm

x_synth_2 += a_rect[0]
x_synth_4 += a_rect[0]
x_synth_6 += a_rect[0]

plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.stem(range(7), A_rect[:7], basefmt=" ")
plt.title('Спектр амплитуд (до 6 гармоники)')
plt.grid(True)

plt.subplot(2, 2, 2)
plt.stem(range(7), phi_rect[:7], basefmt=" ")
plt.title('Спектр фаз (до 6 гармоники)')
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(t_synth, x_rect[:len(t_synth)], 'k--', label='Оригинал', alpha=0.5)
plt.plot(t_synth, x_synth_2, label='Сумма 2 гармоник')
plt.plot(t_synth, x_synth_4, label='Сумма 4 гармоник')
plt.plot(t_synth, x_synth_6, label='Сумма 6 гармоник')
plt.title('Синтез прямоугольного сигнала')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

f1 = 1.0
T_orth = 1 / f1
t3 = np.linspace(0, T_orth, 10000)

s1 = np.sin(2 * np.pi * 1 * f1 * t3)
s2 = np.sin(2 * np.pi * 2 * f1 * t3)
s3 = np.sin(2 * np.pi * 3 * f1 * t3)

int_12 = integrate(s1 * s2, t3)
int_13 = integrate(s1 * s3, t3)
print(f"Интеграл s1*s2 (кратные частоты): {int_12:.5f} (должно быть ~0)")
print(f"Интеграл s1*s3 (кратные частоты): {int_13:.5f} (должно быть ~0)")

s_non = np.sin(2 * np.pi * 1.5 * f1 * t3)
int_non = integrate(s1 * s_non, t3)
print(f"Интеграл s1*s_non (не кратная частота): {int_non:.5f} (НЕ равно 0)")

t_short = np.linspace(0, 0.8 * T_orth, 8000)
s1_short = np.sin(2 * np.pi * 1 * f1 * t_short)
s2_short = np.sin(2 * np.pi * 2 * f1 * t_short)
int_short = integrate(s1_short * s2_short, t_short)
print(f"Интеграл на интервале 0.8T: {int_short:.5f} (НЕ равно 0)")

k, n = 2, 3
sk_c = np.exp(1j * 2 * np.pi * k * f1 * t3)
sn_c = np.exp(1j * 2 * np.pi * n * f1 * t3)
int_c = integrate(sk_c * np.conj(sn_c), t3)
print(f"Интеграл комплексных exp(j2π2t) * exp(-j2π3t): {np.abs(int_c):.5f} (должно быть ~0)")

cases = [
    {"T": 0.1, "tau": 0.05, "label": "T=0.1, τ=0.05 (скв=2)"},
    {"T": 0.1, "tau": 0.025, "label": "T=0.1, τ=0.025 (скв=4)"},
    {"T": 0.2, "tau": 0.05, "label": "T=0.2, τ=0.05 (скв=4)"}
]

n_harm = np.arange(1, 20)
plt.figure(figsize=(10, 6))

for case in cases:
    T_c = case["T"]
    tau_c = case["tau"]
    f0_c = 1 / T_c
    A_n_theory = (2 * 1.0 * tau_c / T_c) * np.abs(np.sinc(n_harm * f0_c * tau_c))
    plt.plot(n_harm * f0_c, A_n_theory, marker='o', label=case["label"])

plt.title('Спектры последовательности прямоугольных видеоимпульсов')
plt.xlabel('Частота, Гц')
plt.ylabel('Амплитуда гармоники')
plt.legend()
plt.grid(True)
plt.show()
