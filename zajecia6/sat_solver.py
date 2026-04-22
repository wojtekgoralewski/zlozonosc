import itertools

def evaluate_formula(assignment, formula):
    """Sprawdza, czy dane wartościowanie spełnia formułę CNF."""
    for clause in formula:
        clause_satisfied = False
        for literal in clause:
            var_index = abs(literal) - 1
            value = assignment[var_index]
            
            if literal < 0:
                value = not value
                
            if value:
                clause_satisfied = True
                break
        
        if not clause_satisfied:
            return False
    return True

def solve_sat(n, formula):
    # Generowanie wszystkich możliwych wartościowań T = x1, x2, xn
    for assignment in itertools.product([False, True], repeat=n):   
        if evaluate_formula(assignment, formula):
            return True
    return False