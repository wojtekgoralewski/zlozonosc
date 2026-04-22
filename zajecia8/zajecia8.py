def get_var(i, j, n):
    """
    Mapuje zmienną logiczną x_{i,j} na unikalną liczbę całkowitą dla formatu DIMACS.
    i - pozycja na ścieżce (od 1 do n)
    j - numer wierzchołka (od 1 do n)
    """
    return (i - 1) * n + j

def hamiltonian_path_to_sat(n, edges, directed=False):
    clauses = []
    
    edge_set = set()
    for u, v in edges:
        edge_set.add((u, v))
        if not directed:
            edge_set.add((v, u))

    # 1. Dla każdego j: j musi pojawić się na ścieżce
    # (x_{1,j} v x_{2,j} v ... v x_{n,j})
    for j in range(1, n + 1):
        clause = [get_var(i, j, n) for i in range(1, n + 1)]
        clauses.append(clause)

    # 2. Dla każdej pary i != k: wierzchołek j nie może być na dwóch pozycjach naraz
    # (-x_{i,j} v -x_{k,j})
    for j in range(1, n + 1):
        for i in range(1, n + 1):
            for k in range(i + 1, n + 1):
                clauses.append([-get_var(i, j, n), -get_var(k, j, n)])

    # 3. Dla każdego i: jakaś pozycja i musi mieć przypisany wierzchołek
    # (x_{i,1} v x_{i,2} v ... v x_{i,n})
    for i in range(1, n + 1):
        clause = [get_var(i, j, n) for j in range(1, n + 1)]
        clauses.append(clause)

    # 4. Dla każdej pary j != k: dwa wierzchołki nie mogą być na tej samej pozycji i
    # (-x_{i,j} v -x_{i,k})
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for k in range(j + 1, n + 1):
                clauses.append([-get_var(i, j, n), -get_var(i, k, n)])

    # 5. Dla każdej pary (u, v) nie będącej krawędzią: 
    # u i v nie mogą być na sąsiadujących pozycjach k oraz k+1
    # (-x_{k,u} v -x_{k+1,v})
    for u in range(1, n + 1):
        for v in range(1, n + 1):
            if u != v and (u, v) not in edge_set:
                for k in range(1, n): # k od 1 do n-1
                    clauses.append([-get_var(k, u, n), -get_var(k + 1, v, n)])

    return clauses

def generate_dimacs(n, clauses):
    num_vars = n * n
    num_clauses = len(clauses)
    
    output = [f"p cnf {num_vars} {num_clauses}"]
    
    for clause in clauses:
        # Każda klauzula kończy się zerem
        clause_str = " ".join(map(str, clause)) + " 0"
        output.append(clause_str)
        
    return "\n".join(output)

if __name__ == "__main__":
    # Definiujemy prosty graf ścieżkowy z 3 wierzchołkami: 1 -- 2 -- 3
    # Ten graf oczywiście posiada ścieżkę Hamiltona (1->2->3)
    V = 3
    E = [(1, 2), (2, 3)]
    
    print(f"Graf: {V} wierzchołki, krawędzie: {E}")
    
    sat_clauses = hamiltonian_path_to_sat(V, E, directed=False)
    dimacs_output = generate_dimacs(V, sat_clauses)
    
    print(dimacs_output)

'''
Pozycja 1: zmienna 1 (wierzchołek 1), 2 (wierzchołek 2), 3 (wierzchołek 3)

Pozycja 2: zmienna 4 (wierzchołek 1), 5 (wierzchołek 2), 6 (wierzchołek 3)

Pozycja 3: zmienna 7 (wierzchołek 1), 8 (wierzchołek 2), 9 (wierzchołek 3)

1 4 7 0 // wierzchołek 1 musi pojawić się na którejś pozycji (1, 2 lub 3)
2 5 8 0 // to samo dla wierzchołka 2
3 6 9 0 // to samo dla wierzchołka 3

-1 -4 0 // wierzchołek 1 nie może zajmować poz. 1 i 2 jednocześnie
-1 -7 0 // ...ani poz. 1 i 3
-4 -7 0 // ...ani poz. 2 i 3
-2 -5 0 // analogiczne zakazy duplikacji dla wierzchołka 2 (jeden wierzchołek = jedno miejsce)
-2 -8 0 
-5 -8 0 
-3 -6 0 // to samo dla wierzchołka 3
-3 -9 0 
-6 -9 0 

1 2 3 0 // 1. pozycja na ścieżce musi być zajęta (przez v1, v2 lub v3)
4 5 6 0 // 2. pozycja musi być zajęta
7 8 9 0 // 3. pozycja musi być zajęta

-1 -2 0 // na 1. pozycji nie mogą stać wierzchołki 1 i 2 naraz
-1 -3 0 // ...ani 1 i 3
-2 -3 0 // ...ani 2 i 3
-4 -5 0 // analogiczne zakazy dla 2. pozycji (tylko jeden wierzchołek na dane miejsce)
-4 -6 0 
-5 -6 0 
-7 -8 0 // to samo dla 3. pozycji
-7 -9 0 
-8 -9 0 

--- zalezy od grafu broni brakującej krawędzi 1-3 ---
-1 -6 0 // zakaz przeskoku z 1 do 3 (na kroku z poz. 1 na 2)
-4 -9 0 // zakaz przeskoku z 1 do 3 (na kroku z poz. 2 na 3)
-3 -4 0 // zakaz przeskoku w drugą stronę: z 3 do 1 (krok 1 -> 2)
-6 -7 0 // zakaz przeskoku z 3 do 1 (krok 2 -> 3)
'''