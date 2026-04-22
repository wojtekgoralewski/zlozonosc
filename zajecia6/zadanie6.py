import json
import time
from sat_solver import solve_sat
from hamilton_solver import solve_hamilton_path

def measure_time(func, *args):
    start_time = time.perf_counter()
    result = func(*args)
    end_time = time.perf_counter()
    return result, end_time - start_time

def main():
    try:
        with open('input.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Nie znaleziono pliku input.json")
        return

    print(f"{'n':<3} | {'Typ Testu':<9} | {'SAT Wynik':<9} | {'SAT Czas (s)':<12} | {'HAM Wynik':<9} | {'HAM Czas (s)':<12}")
    print("-" * 68)

    for case in data['test_cases']:
        n = case['n']
        typ_testu = case.get('typ_testu', 'Nieznany')
        sat_formula = case['sat_formula']
        hamilton_graph = case['hamilton_graph']

        sat_result, sat_time = measure_time(solve_sat, n, sat_formula)

        if typ_testu == "Zlosliwy" and n > 14:
            ham_result = "-"
            ham_time_str = "-"
        else:
            ham_result, ham_time = measure_time(solve_hamilton_path, n, hamilton_graph)
            ham_time_str = f"{ham_time:<12.6f}"

        print(f"{n:<3} | {typ_testu:<9} | {str(sat_result):<9} | {sat_time:<12.6f} | {str(ham_result):<9} | {ham_time_str}")

if __name__ == "__main__":
    main()