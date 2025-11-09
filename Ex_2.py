import time
from math import isqrt
from multiprocessing import Pool, cpu_count

# Функція, яка обчислює дільники одного числа
def factorize_number(n):
    if n == 0:
        return [1]
    divisors = set()
    for i in range(1, isqrt(n) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)
    return sorted(divisors)

def factorize(*numbers):
    result = []
    for n in numbers:
        result.append(factorize_number(n))
    return tuple(result)  # Повертаємо кортеж для розпаковки як у прикладі

# Паралельна версія функції factorize
def factorize_parallel(*numbers):
    with Pool(cpu_count()) as pool:
        result = pool.map(factorize_number, numbers)
    return tuple(result)

if __name__ == "__main__":
    start = time.time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    end = time.time()
    print("Синхронна версія, час виконання:", end - start, "секунд")


    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765,
                 5325530, 10651060]
    print(" Синхронна версія пройшла тести")


    start = time.time()
    a_par, b_par, c_par, d_par = factorize_parallel(128, 255, 99999, 10651060)
    end = time.time()
    print("Паралельна версія, час виконання:", end - start, "секунд")


    assert a_par == a
    assert b_par == b
    assert c_par == c
    assert d_par == d
    print(" Паралельна версія також пройшла тести")
