from collections import deque

def print_graph_adj_list(graph):
    print(">> STRUKTURA GRAFU (SĄSIEDZI) <<")
    for node, neighbors in graph.items():
        if neighbors:
            print(f"   [{node}] ---> {', '.join(map(str, neighbors))}")
        else:
            print(f"   [{node}] ---> (brak)")

def print_capacity_matrix(capacity):
    print(">> MACIERZ PRZEPUSTOWOŚCI <<")
    n = len(capacity)
    
    header = "     | " + " | ".join(f"W{i}" for i in range(n)) + " |"
    separator = "-" * len(header)
    
    print(separator)
    print(header)
    print(separator)
    
    for i, row in enumerate(capacity):
        row_str = " | ".join(f"{x:2}" for x in row)
        print(f"  W{i} | {row_str} |")
    print(separator)


def reachable(graph, start, target):
    visited = set()
    queue = deque([start])

    while queue:
        v = queue.popleft()
        if v == target:
            return True
        for u in graph[v]:
            if u not in visited:
                visited.add(u)
                queue.append(u)

    return False


def bfs(capacity, flow, s, t, parent):
    n = len(capacity)
    visited = [False] * n
    queue = deque([s])
    visited[s] = True

    while queue:
        u = queue.popleft()
        for v in range(n):
            if not visited[v] and capacity[u][v] - flow[u][v] > 0:
                parent[v] = u
                visited[v] = True
                queue.append(v)

    return visited[t]

def max_flow(capacity, s, t):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    parent = [-1] * n
    maxflow = 0

    while bfs(capacity, flow, s, t, parent):
        path_flow = float('inf')
        v = t

        while v != s:
            u = parent[v]
            path_flow = min(path_flow, capacity[u][v] - flow[u][v])
            v = u

        v = t
        while v != s:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u

        maxflow += path_flow

    return maxflow


def bipartite_matching(U_size, V_size, edges):
    n = U_size + V_size + 2
    s = n - 2
    t = n - 1

    capacity = [[0] * n for _ in range(n)]

    # s → U
    for u in range(U_size):
        capacity[s][u] = 1

    # U → V
    for u, v in edges:
        capacity[u][U_size + v] = 1

    # V → t
    for v in range(V_size):
        capacity[U_size + v][t] = 1

    return capacity, max_flow(capacity, s, t)


if __name__ == "__main__":
    
    # ---------------------------------------------------------
    print("\n" + "="*50)
    print(" TEST 1: OSIĄGALNOŚĆ (REACHABILITY) ")
    print("="*50)
    
    graph = {
        0: [1, 2],
        1: [3],
        2: [],
        3: []
    }
    v_from, v_to = 0, 3
    
    print_graph_adj_list(graph)
    result = reachable(graph, v_from, v_to)
    
    status = "TAK (Ścieżka istnieje)" if result else "NIE (Brak przejścia)"
    print(f"\n[WYNIK] Cel: węzeł {v_from} -> węzeł {v_to}")
    print(f"[WYNIK] Czy można dotrzeć? : {status}")

    # ---------------------------------------------------------
    print("\n\n" + "="*50)
    print(" TEST 2: MAKSYMALNY PRZEPŁYW (MAX FLOW) ")
    print("="*50)
    
    capacity = [
        [0, 3, 2, 0],
        [0, 0, 5, 2],
        [0, 0, 0, 3],
        [0, 0, 0, 0]
    ]
    
    print_capacity_matrix(capacity)
    result = max_flow(capacity, 0, 3)
    
    print(f"\n[WYNIK] Wyliczony maksymalny przepływ sieci: {result}")

    # ---------------------------------------------------------
    print("\n\n" + "="*50)
    print(" TEST 3: SKOJARZENIA (BIPARTITE MATCHING) ")
    print("="*50)
    
    edges = [(0, 0), (0, 1), (1, 1)]
    capacity, result = bipartite_matching(2, 2, edges)
    
    print_capacity_matrix(capacity)
    print(f"\n[WYNIK] Rozmiar maksymalnego skojarzenia wynosi: {result}")
    print("\n" + "="*50 + "\n")