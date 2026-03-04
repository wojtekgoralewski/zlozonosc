import re

def to_bin(n): return bin(n)[2:]
def from_bin(b): return int(b, 2)

def build_lecture(n, edges):
    v_str = "(" + ",".join([f"[{to_bin(i)}]" for i in range(1, n + 1)]) + ")"
    e_str = "(" + ",".join([f"([{to_bin(u)}],[{to_bin(v)}])" for u, v in edges]) + ")"
    return f"({v_str},{e_str})"

def build_matrix(n, edges):
    matrix = [[0]*n for _ in range(n)]
    for u, v in edges:
        matrix[u-1][v-1] = 1
        matrix[v-1][u-1] = 1 
    return f"M=({n},[" + ",".join(["".join(map(str, row)) for row in matrix]) + "])"

def encode_instance():
    while True:
        try:
            n = int(input("Liczba wierzchołków (V=3q): "))
            if n > 0 and n % 3 == 0: break
        except ValueError: pass
        print("Błąd: Wymagana dodatnia wielokrotność 3.")

    try: m = int(input("Liczba krawędzi: "))
    except ValueError: m = 0

    edges = []
    i = 0
    while i < m:
        try:
            u, v = map(int, input(f"Krawędź {i+1}/{m} (u v): ").split())
            if 1 <= u <= n and 1 <= v <= n and u != v:
                edge = (min(u, v), max(u, v))
                if edge not in edges:
                    edges.append(edge)
                    i += 1
                else: print("Błąd: Duplikat.")
            else: print(f"Błąd: Nieprawidłowe wierzchołki (1-{n}) lub pętla.")
        except ValueError: print("Błąd: Podaj dwie liczby.")

    wybor = input("Format (1-Wykładowy, 2-Macierz): ")
    chain = build_lecture(n, edges) if wybor == "1" else build_matrix(n, edges)
    
    print(f"\nZakodowany łańcuch:\n{chain}\n")
    return chain

def parse_chain(chain):
    """Zwraca krotkę: (liczba wierzchołków, lista krawędzi, nazwa_formatu)"""
    chain = chain.strip()
    if chain.startswith("M="):
        match = re.search(r'M=\((\d+),\[(.*?)\]\)', chain)
        n = int(match.group(1))
        rows = match.group(2).split(',')
        edges = [(i+1, j+1) for i in range(n) for j in range(i+1, n) if rows[i][j] == '1']
        return n, edges, "macierz"
    elif chain.startswith("("):
        v_part = re.search(r'^\(\((.*?)\),', chain).group(1)
        vertices = [from_bin(b) for b in re.findall(r'\[([01]+)\]', v_part)]
        e_part = re.search(r',(\(.*?\)\))$', chain).group(1)
        edges = [(from_bin(u), from_bin(v)) for u, v in re.findall(r'\(\[([01]+)\],\[([01]+)\]\)', e_part)]
        return len(vertices), edges, "wykładowy"
    raise ValueError("Nieznany format.")

def decode_instance(chain):
    try:
        n, edges, fmt = parse_chain(chain)
        print(f"\nWynik odkodowania ({fmt}):\nV: {list(range(1, n+1))}\nE: {edges}")
    except Exception: print("Błąd: Uszkodzony łańcuch.\n")

def translate_instance(chain):
    try:
        n, edges, fmt = parse_chain(chain)
        if fmt == "macierz":
            new_chain = build_lecture(n, edges)
            print(f"\nPrzetłumaczono na format binarny:\n{new_chain}\n")
        else:
            new_chain = build_matrix(n, edges)
            print(f"\nPrzetłumaczono na macierz:\n{new_chain}\n")
        return new_chain
    except Exception: print("Błąd translacji.\n")

def menu():
    last_chain = ""
    while True:
        wybor = input("1. Zakoduj | 2. Dekoduj | 3. Tłumacz (Macierz <-> Binarny) | 4. Wyjście -> ")
        if wybor == "1":
            last_chain = encode_instance()
        elif wybor in ("2", "3"):
            s = input("Wklej łańcuch (Enter = użyj ostatniego): ")
            chain = s if s else last_chain
            if chain:
                if wybor == "2": decode_instance(chain)
                else: last_chain = translate_instance(chain)
            else: print("Brak łańcucha do operacji.\n")
        elif wybor == "4":
            break

if __name__ == "__main__":
    menu()