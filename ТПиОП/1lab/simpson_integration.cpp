#include <iostream>
#include <fstream>
#include <cmath>
#include <omp.h>
#include <iomanip>
#include <vector>
#include <chrono>
#include <windows.h>

using namespace std;

// Подынтегральная функция f(x) = x/sin³(2x)
double f(double x) {
    return x / pow(sin(2.0 * x), 3);
}

// Метод Симпсона для фиксированного числа разбиений
double simpson(double a, double b, int n) {
    if (n % 2 != 0) n++;
    
    double h = (b - a) / n;
    double sum = f(a) + f(b);
    
    #pragma omp parallel for reduction(+:sum)
    for (int i = 1; i < n; i++) {
        double x = a + i * h;
        if (i % 2 == 0)
            sum += 2.0 * f(x);
        else
            sum += 4.0 * f(x);
    }
    
    return (h / 3.0) * sum;
}

// Метод Симпсона с правилом Рунге
double simpson_runge(double a, double b, double epsilon, int& n_final) {
    int n = 10;
    double prev_result = simpson(a, b, n);
    double curr_result;
    
    for (int iter = 1; iter < 30; iter++) {
        n *= 2;
        curr_result = simpson(a, b, n);
        
        double error = fabs(curr_result - prev_result) / 15.0;
        
        if (error < epsilon) {
            n_final = n;
            return curr_result;
        }
        
        prev_result = curr_result;
    }
    
    n_final = n;
    return curr_result;
}

// Измерение времени с высокой точностью (в секундах)
double get_time() {
    LARGE_INTEGER freq, counter;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&counter);
    return (double)counter.QuadPart / (double)freq.QuadPart;
}

// Функция для тестирования масштабируемости
double test_scalability(double a, double b, int n, int num_threads) {
    double h = (b - a) / n;
    double sum = f(a) + f(b);
    
    #pragma omp parallel for num_threads(num_threads) reduction(+:sum)
    for (int i = 1; i < n; i++) {
        double x = a + i * h;
        if (i % 2 == 0)
            sum += 2.0 * f(x);
        else
            sum += 4.0 * f(x);
    }
    
    return (h / 3.0) * sum;
}

int main() {
    // Исправление кодировки для Windows
    SetConsoleOutputCP(65001);
    setlocale(LC_ALL, "Russian");
    
    double a = 0.1;
    double b = 0.5;
    double epsilon = 1e-6;
    
    int n_final;
    
    cout << "========================================" << endl;
    cout << "Numerical integration (Simpson + OpenMP)" << endl;
    cout << "========================================" << endl;
    cout << endl;
    cout << "Parameters:" << endl;
    cout << "  f(x) = x/sin^3(2x)" << endl;
    cout << "  Interval: [" << a << "; " << b << "]" << endl;
    cout << "  Precision epsilon = " << epsilon << endl;
    cout << endl;
    
    // Вычисление интеграла
    double result = simpson_runge(a, b, epsilon, n_final);
    
    cout << "Results:" << endl;
    cout << "  Integral value: " << setprecision(10) << result << endl;
    cout << "  Number of partitions: " << n_final << endl;
    cout << endl;
    
    // Тестирование масштабируемости
    // Используем большое число разбиений для измеримого времени
    int n_test = 100000000;  // 100 миллионов разбиений
    int num_repeats = 5;     // Повторений для усреднения
    
    cout << "========================================" << endl;
    cout << "Scalability analysis" << endl;
    cout << "  Test partitions: " << n_test << endl;
    cout << "  Repeats: " << num_repeats << endl;
    cout << "========================================" << endl;
    cout << endl;
    
    vector<int> threads_list = {1, 2, 4, 16, 32, 64};
    vector<double> avg_times;
    
    cout << fixed << setprecision(6);
    cout << setw(10) << "Threads" << setw(18) << "Time(sec)" 
         << setw(18) << "Speedup" << setw(18) << "Efficiency" << endl;
    cout << "----------------------------------------------------------------" << endl;
    
    double base_time = 0;
    
    for (int num_threads : threads_list) {
        // Усреднение по нескольким запускам
        vector<double> times;
        for (int r = 0; r < num_repeats; r++) {
            double t_start = get_time();
            test_scalability(a, b, n_test, num_threads);
            double t_end = get_time();
            times.push_back(t_end - t_start);
        }
        
        // Берем минимальное время (наиболее чистый замер)
        double min_time = times[0];
        for (double t : times) {
            if (t < min_time) min_time = t;
        }
        
        avg_times.push_back(min_time);
        
        if (num_threads == 1) {
            base_time = min_time;
        }
        
        double speedup = base_time / min_time;
        double efficiency = speedup / num_threads * 100.0;
        
        cout << setw(10) << num_threads << setw(18) << min_time 
             << setw(18) << speedup << setw(17) << efficiency << "%" << endl;
    }
    
    cout << endl;
    
    // Сохранение данных для графика
    ofstream graph_data("scalability_data.txt");
    graph_data << "# Threads Time Speedup Efficiency" << endl;
    for (size_t i = 0; i < threads_list.size(); i++) {
        double speedup = avg_times[0] / avg_times[i];
        double efficiency = speedup / threads_list[i] * 100.0;
        graph_data << threads_list[i] << " " << avg_times[i] << " " 
                   << speedup << " " << efficiency << endl;
    }
    graph_data.close();
    
    cout << "Data saved to 'scalability_data.txt'" << endl;
    
    return 0;
}