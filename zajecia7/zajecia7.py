import time
import math

def is_prime_exact(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def sieve_of_eratosthenes(limit):
    if limit < 2:
        return []
    primes = [True] * (limit + 1)
    primes[0] = primes[1] = False
    for p in range(2, int(math.sqrt(limit)) + 1):
        if primes[p]:
            for i in range(p * p, limit + 1, p):
                primes[i] = False
    return primes

def compare_algorithms():
    print(f"{'Bity':<6} | {'Liczba (n)':<12} | {'Dokładny (s)':<15} | {'Sito (s)':<15}")
    print("-" * 55)
    
    for b in range(2, 50):
        n = (1 << b) - 1
        # Algorytm dokładny
        start_exact = time.perf_counter()
        is_prime_exact(n)
        end_exact = time.perf_counter()
        time_exact = end_exact - start_exact
        
        # Sito Erastotenesa
        start_sieve = time.perf_counter()
        sieve_of_eratosthenes(n)
        end_sieve = time.perf_counter()
        time_sieve = end_sieve - start_sieve
        
        print(f"{b:<6} | {n:<12} | {time_exact:<15.6f} | {time_sieve:<15.6f}")
        
        if time_exact > 60 or time_sieve > 60:
            break

if __name__ == "__main__":
    compare_algorithms()