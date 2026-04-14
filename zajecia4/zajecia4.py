import time
import random
import sys

# 1. Algorytm Dokładny (Brute Force) - Wykładniczy O(2^n)
# Sprawdzamy rekurencyjnie każdą możliwą kombinację (biore / nie biorę)
def brute_force(items, capacity, n):
    if n == 0 or capacity == 0:
        return 0
    
    val, weight = items[n-1]
    
    if weight > capacity:
        return brute_force(items, capacity, n-1)
    else:
        return max(
            val + brute_force(items, capacity - weight, n-1), # Biorę
            brute_force(items, capacity, n-1)                 # Nie biorę
        )

# 2. Algorytm Dynamiczny (DP) - Pseudowielomianowy O(n * M)
def dp_knapsack(items, M):
    n = len(items)
    # Tworzymy tabelę A[n+1][M+1] wypełnioną zerami
    A = [[0 for _ in range(M + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        val, weight = items[i-1]
        for w in range(M + 1):
            if weight <= w:
                A[i][w] = max(A[i-1][w], A[i-1][w - weight] + val)
            else:
                A[i][w] = A[i-1][w]
    return A[n][M]

def run_test():
    print("=== Eksperyment: Problem Plecakowy ===")
    try:
        max_n = int(input("Podaj maksymalną liczbę przedmiotów (n): "))
        max_M = int(input("Podaj maksymalną pojemność plecaka (M): "))
    except ValueError:
        print("Błąd: Podaj liczbę całkowitą!")
        return

    print(f"\n{'n':>3} | {'M':>3} | {'Brute Force (s)':>15} | {'Dynamic (s)':>15}")
    print("-" * 55)

    for n in range(1, max_n + 1):
        # Generujemy przedmioty (wartość, waga) z zakresu 1-10
        items = [(random.randint(1, 10), random.randint(1, 10)) for _ in range(n)]
        
        for M in range(1, max_M + 1):
            # Pomiar Brute Force
            start_bf = time.perf_counter()
            res_bf = brute_force(items, M, n)
            end_bf = time.perf_counter() - start_bf

            # Pomiar DP
            start_dp = time.perf_counter()
            res_dp = dp_knapsack(items, M)
            end_dp = time.perf_counter() - start_dp

            # Wypisywanie wyników na bieżąco
            print(f"{n:3d} | {M:3d} | {end_bf:15.8f} | {end_dp:15.8f}")
            
            # Flush sprawia, że tekst pojawia się w konsoli natychmiast
            sys.stdout.flush()

if __name__ == "__main__":
    run_test()