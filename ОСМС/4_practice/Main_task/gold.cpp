// =====================================================================
//  Практическая работа No4 (Занятие No4). Коды Голда: генерация и
//  корреляционные свойства (C/C++).
//  Схема генератора - рисунок 4.5 (вариант для НЕЧЁТНОГО номера группы;
//  группа ИКС-431).
//
//  Два 5-разрядных сдвиговых регистра (Fibonacci LFSR), сдвиг вправо.
//    x-регистр: обратная связь new_x1 = x4 XOR x5 ; выход = x5
//    y-регистр: обратная связь new_y1 = y2 XOR y5 ; выход = y5
//    Код Голда = x5 XOR y5.  Длина = 2^5 - 1 = 31.
//
//  Начальные состояния: x = номер в журнале (5 бит), y = x + 7 (5 бит).
//  Шаг 3: второй код Голда при x = x+1, y = y-5.
// =====================================================================
#include <cstdio>
#include <cstdint>

#ifndef JOURNAL_NUM
#define JOURNAL_NUM 18          // <<< ПОРЯДКОВЫЙ НОМЕР В ЖУРНАЛЕ (замените на свой)
#endif

static const int M   = 5;                 // число разрядов регистра
static const int LEN = (1 << M) - 1;      // длина m- / Голда-последовательности = 31

// 5-битное представление числа: bits[0]=x1 (старший разряд) ... bits[4]=x5
static void to_bin(int v, int bits[M]) {
    for (int i = 0; i < M; ++i)
        bits[i] = (v >> (M - 1 - i)) & 1;
}

// Генерация одной последовательности Голда (схема рис. 4.5) по начальным
// значениям xval, yval. out[] заполняется LEN битами.
static void gold(int xval, int yval, int out[LEN]) {
    int x[M], y[M];
    to_bin(xval, x);
    to_bin(yval, y);
    for (int n = 0; n < LEN; ++n) {
        out[n] = x[M - 1] ^ y[M - 1];     // x5 XOR y5
        int fb_x = x[3] ^ x[4];           // x4 XOR x5 (отводы 4,5)
        int fb_y = y[1] ^ y[4];           // y2 XOR y5 (отводы 2,5)
        for (int i = M - 1; i > 0; --i) { // сдвиг вправо
            x[i] = x[i - 1];
            y[i] = y[i - 1];
        }
        x[0] = fb_x;
        y[0] = fb_y;
    }
}

// Циклическая автокорреляция (формула 4.3): (совпадения - несовпадения)/LEN.
static double autocorr(const int s[LEN], int tau) {
    int match = 0;
    for (int i = 0; i < LEN; ++i) {
        int j = (i + tau) % LEN;
        if (s[i] == s[j]) ++match;
    }
    return double(match - (LEN - match)) / LEN;
}

// Циклическая взаимная корреляция двух последовательностей при сдвиге tau.
static double crosscorr(const int a[LEN], const int b[LEN], int tau) {
    int match = 0;
    for (int i = 0; i < LEN; ++i) {
        int j = (i + tau) % LEN;
        if (a[i] == b[j]) ++match;
    }
    return double(match - (LEN - match)) / LEN;
}

// Печать последовательности слитной строкой бит.
static void print_seq(const char* label, const int s[LEN]) {
    printf("%s", label);
    for (int i = 0; i < LEN; ++i) printf("%d", s[i]);
    printf("\n");
}

int main() {
    int xval = JOURNAL_NUM;
    int yval = xval + 7;                  // y = x + 7
    int yval_5bit = yval & 0x1F;          // ограничение 5 битами (mod 32)

    printf("================================================================\n");
    printf(" ПР No4. Код Голда (схема рис. 4.5, нечётная группа).\n");
    printf(" Номер в журнале x = %d, y = x+7 = %d\n", xval, yval);
    if (yval_5bit != yval)
        printf(" ВНИМАНИЕ: y=x+7=%d > 31, берём 5 бит -> y = %d\n", yval, yval_5bit);

    int xb[M], yb[M];
    to_bin(xval, xb); to_bin(yval_5bit, yb);
    printf(" x (5 бит) ="); for (int i=0;i<M;++i) printf(" %d", xb[i]); printf("\n");
    printf(" y (5 бит) ="); for (int i=0;i<M;++i) printf(" %d", yb[i]); printf("\n");

    // ---- Шаг 1: генерация и вывод последовательности Голда ----
    int g[LEN];
    gold(xval, yval_5bit, g);
    printf("\n[Шаг 1] Последовательность Голда (длина %d):\n", LEN);
    print_seq("  ", g);

    // ---- Шаг 2: циклический сдвиг + автокорреляция (таблица) ----
    printf("\n[Шаг 2] Автокорреляция при циклических сдвигах (формула 4.3):\n");
    printf("  Сдвиг | Сдвинутая последовательность            | Автокорр.\n");
    printf("  ------+-----------------------------------------+---------\n");
    for (int tau = 0; tau < LEN; ++tau) {
        printf("  %5d | ", tau);
        for (int i = 0; i < LEN; ++i) printf("%d", g[(i + tau) % LEN]);
        printf(" | %+.4f\n", autocorr(g, tau));
    }

    // ---- Шаг 3: второй код Голда при x=x+1, y=y-5 ----
    int x2val = xval + 1;
    int y2val = (yval - 5) & 0x1F;        // y-5, ограничение 5 битами
    int g2[LEN];
    gold(x2val, y2val, g2);
    printf("\n[Шаг 3] Второй код Голда: x=x+1=%d, y=y-5=%d\n", x2val, yval - 5);
    print_seq("  ", g2);

    // ---- Шаг 4: взаимная корреляция исходной и новой последовательностей ----
    printf("\n[Шаг 4] Взаимная корреляция g и g2 (циклическая):\n");
    printf("  R_cross(tau=0) = %+.4f\n", crosscorr(g, g2, 0));
    double mx = -2.0, mn = 2.0;
    for (int tau = 0; tau < LEN; ++tau) {
        double r = crosscorr(g, g2, tau);
        if (r > mx) mx = r;
        if (r < mn) mn = r;
    }
    printf("  Диапазон по всем сдвигам: [%.4f ; %.4f]\n", mn, mx);

    printf("\n================================================================\n");
    return 0;
}
