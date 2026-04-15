def solve_hamilton_path(n, graph):
    """
    Rozwiązuje problem HAMILTON PATH przeszukując graf DFS-em.
    Zwraca True, jeśli ścieżka istnieje, w przeciwnym razie False.
    """
    visited = set()

    def dfs(current_node):
        visited.add(current_node)
        
        if len(visited) == n:
            visited.remove(current_node)
            return True
            
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
                    
        visited.remove(current_node)
        return False

    for start_node in range(n):
        if dfs(start_node):
            return True
            
    return False