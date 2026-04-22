import pycosat

def get_var(i, j, n):
    return (i - 1) * n + j

def hamiltonian_path_to_sat(n, edges, directed=False):
    clauses = []
    edge_set = set()
    
    for u, v in edges:
        edge_set.add((u, v))
        if not directed:
            edge_set.add((v, u))

    for j in range(1, n + 1):
        clauses.append([get_var(i, j, n) for i in range(1, n + 1)])

    for j in range(1, n + 1):
        for i in range(1, n + 1):
            for k in range(i + 1, n + 1):
                clauses.append([-get_var(i, j, n), -get_var(k, j, n)])

    for i in range(1, n + 1):
        clauses.append([get_var(i, j, n) for j in range(1, n + 1)])

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for k in range(j + 1, n + 1):
                clauses.append([-get_var(i, j, n), -get_var(i, k, n)])

    for u in range(1, n + 1):
        for v in range(1, n + 1):
            if u != v and (u, v) not in edge_set:
                for k in range(1, n): 
                    clauses.append([-get_var(k, u, n), -get_var(k + 1, v, n)])

    return clauses

def decode_solution(solution, n):
    path = [0] * n
    for var in solution:
        if var > 0:
            i = (var - 1) // n + 1
            j = (var - 1) % n + 1
            path[i - 1] = j
    return " -> ".join(map(str, path))

def find_hamiltonian_path_dfs(n, edges, directed=False):
    adj = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)

    def dfs(path):
        if len(path) == n:
            return path
        for neighbor in adj[path[-1]]:
            if neighbor not in path:
                res = dfs(path + [neighbor])
                if res:
                    return res
        return None

    for start_node in range(1, n + 1):
        res = dfs([start_node])
        if res:
            return res
            
    return None

def run_test(V, E):
    clauses = hamiltonian_path_to_sat(V, E)
    
    hamilton_path_raw = find_hamiltonian_path_dfs(V, E)
    has_hamilton = hamilton_path_raw is not None

    sat_solution = pycosat.solve(clauses)
    is_sat = sat_solution != "UNSAT"

    dfs_res = " -> ".join(map(str, hamilton_path_raw)) if has_hamilton else "Brak"
    sat_res = decode_solution(sat_solution, V) if is_sat else "Brak"

    print(f"\nV={V}, E={E}")
    print(f" DFS  : {dfs_res}")
    print(f" SAT  : {sat_res}")
    
    for clause in clauses:
        print(" ".join(map(str, clause)) + " 0")

if __name__ == "__main__":
    run_test(3, [(1, 2), (2, 3)])
    run_test(4, [(1, 2), (1, 3), (1, 4)])
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


