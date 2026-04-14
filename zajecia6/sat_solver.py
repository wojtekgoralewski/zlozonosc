import itertools

def evaluate_formula(assignment, formula):
    """Sprawdza, czy dane wartościowanie spełnia formułę CNF."""
    for clause in formula:
        clause_satisfied = False
        for literal in clause:
            # Zmienne są od 1 do n. Indeks w krotce to abs(literal) - 1.
            var_index = abs(literal) - 1
            value = assignment[var_index]
            
            # Jeśli literał jest ujemny (np. -1), odwracamy wartość logiczną
            if literal < 0:
                value = not value
                
            if value:
                clause_satisfied = True
                break
        
        # Jeśli jakakolwiek klauzula nie jest spełniona, cała formuła jest fałszywa
        if not clause_satisfied:
            return False
    return True

def solve_sat(n, formula):
    """
    Rozwiązuje problem SAT algorytmem dokładnym (brute-force).
    Zwraca True, jeśli formuła jest spełnialna, w przeciwnym razie False.
    """
    # Generowanie wszystkich możliwych wartościowań T = (x1, x2, ..., xn)
    for assignment in itertools.product([False, True], repeat=n):
        if evaluate_formula(assignment, formula):
            return True
    return False