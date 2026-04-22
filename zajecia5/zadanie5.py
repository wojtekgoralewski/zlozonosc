from collections import deque

def print_graph_adj_list(graph):
    print("STRUKTURA GRAFU (SĄSIEDZI)")
    for node, neighbors in graph.items():
        if neighbors:
            print(f"   [{node}] ---> {', '.join(map(str, neighbors))}")
        else:
            print(f"   [{node}] ---> (brak)")

def print_capacity_matrix(capacity):
    print("MACIERZ PRZEPUSTOWOŚCI")
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


def reachable(capacity, flow, start, target, parent):
    n = len(capacity)
    visited = [False] * n
    queue = deque([start])
    visited[start] = True

    while queue:
        u = queue.popleft()
        if u == target:
            return True
        for v in range(n):
            if not visited[v] and capacity[u][v] - flow[u][v] > 0:
                parent[v] = u
                visited[v] = True
                queue.append(v)
    return False

def max_flow(capacity, s, t):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    parent = [-1] * n
    maxflow = 0
    
    while reachable(capacity, flow, s, t, parent):
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
        parent = [-1] * n

    return maxflow

def bipartite_matching(U_size, V_size, edges):
    n = U_size + V_size + 2
    s = n - 2
    t = n - 1
    capacity = [[0] * n for _ in range(n)]

    for u in range(U_size):
        capacity[s][u] = 1
    for u, v in edges:
        capacity[u][U_size + v] = 1
    for v in range(V_size):
        capacity[U_size + v][t] = 1

    return capacity, max_flow(capacity, s, t)


if __name__ == "__main__":
    print("\n" + "="*50)
    print(" TEST 1: OSIĄGALNOŚĆ (REACHABILITY) ")
    print("="*50)
    
    graph_capacity = [[0, 1, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0]]
    graph_flow = [[0]*4 for _ in range(4)]
    parent = [-1]*4
    
    result = reachable(graph_capacity, graph_flow, 0, 3, parent)
    
    status = "Ścieżka istnieje" if result else "NIE (Brak przejścia)"
    print(f"\n węzeł 0 -> węzeł 3")
    print(f" {status}")

    print("\n\n" + "="*50)
    print(" TEST 2: MAKSYMALNY PRZEPŁYW (MAX FLOW) ")
    print("="*50)
    
    cap = [
        [0, 3, 2, 0],
        [0, 0, 5, 2],
        [0, 0, 0, 3],
        [0, 0, 0, 0]
    ]
    print_capacity_matrix(cap)
    res_flow = max_flow(cap, 0, 3)
    print(f"\n Wyliczony maksymalny przepływ sieci: {res_flow}")

    print("\n\n" + "="*50)
    print(" TEST 3:  MATCHING ")
    print("="*50)
    
    match_edges = [(0, 0), (0, 1), (1, 1)]
    cap_match, res_match = bipartite_matching(2, 2, match_edges)
    print_capacity_matrix(cap_match)
    print(f"\nRozmiar maksymalnego skojarzenia wynosi: {res_match}")
    print("\n" + "="*50 + "\n")