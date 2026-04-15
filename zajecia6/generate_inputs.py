import json
import random

def generate_sat_formula(n):
    num_clauses = max(2, int(2.5 * n))
    formula = []
    for _ in range(num_clauses):
        clause_length = random.randint(1, min(3, n))
        vars_in_clause = random.sample(range(1, n + 1), clause_length)
        clause = [v if random.choice([True, False]) else -v for v in vars_in_clause]
        formula.append(clause)
    return formula

def generate_hamilton_graph(n):
    graph = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and random.random() < 0.30:  
                graph[i].append(j)
    return graph

def generate_worst_case_hamilton_graph(n):
    if n < 4: return [[] for _ in range(n)]
    size_a = (n // 2) - 1
    A = list(range(0, size_a))
    B = list(range(size_a, n))
    graph = [[] for _ in range(n)]
    for u in A:
        for v in B:
            graph[u].append(v)
            graph[v].append(u) 
    return graph

def generate_malicious_sat(n):
    formula = []
    for i in range(1, n + 1):
        for _ in range(n):
            formula.append([i, -i]) 
    formula.append([1])
    formula.append([-1])
    return formula

def main():
    test_cases = []
    
    for n in range(1, 21):
        # 1. Wiersz: Losowy (dla SAT i HAM)
        test_cases.append({
            "n": n,
            "typ_testu": "Losowy",
            "sat_formula": generate_sat_formula(n),
            "hamilton_graph": generate_hamilton_graph(n)
        })
        
        # 2. Wiersz: Złośliwy (dla SAT i HAM)
        test_cases.append({
            "n": n,
            "typ_testu": "Zlosliwy",
            "sat_formula": generate_malicious_sat(n),
            "hamilton_graph": generate_worst_case_hamilton_graph(n) if n <= 14 else []
        })

    with open('input.json', 'w') as file:
        json.dump({"test_cases": test_cases}, file, indent=2)
        
    print("Wygenerowano plik input.json z parami testów: Losowy i Złośliwy!")

if __name__ == "__main__":
    main()