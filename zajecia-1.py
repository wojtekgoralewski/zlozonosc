import re

def to_bin(n):
    return bin(n)[2:]

def from_bin(b):
    return int(b, 2)

def encode_instance():
    print("\n--- TWORZENIE INSTANCJI (KODOWANIE) ---")
    
    # 1. Pobieranie danych i walidacja V = 3q
    while True:
        try:
            n = int(input("Podaj liczbę wierzchołków (musi być podzielna przez 3, np. 3, 6, 9): "))
            if n > 0 and n % 3 == 0: break
            print("BŁĄD: Liczba wierzchołków musi być dodatnią wielokrotnością 3!")
        except ValueError:
            print("BŁĄD: Wprowadzono niepoprawne dane.")

    try:
        m = int(input("Podaj liczbę krawędzi: "))
    except ValueError:
        m = 0

    # 2. Zbieranie surowych krawędzi z walidacją
    raw_edges = []
    print(f"Wprowadź krawędzie (wierzchołki od 1 do {n}):")
    for i in range(m):
        while True:
            try:
                u, v = map(int, input(f"Krawędź {i+1}/{m} (np. '1 2'): ").split())
                if 1 <= u <= n and 1 <= v <= n:
                    if u != v: # ignorujemy pętle
                        raw_edges.append((u, v))
                    break
                else:
                    print(f"BŁĄD: Wierzchołki muszą być w zakresie od 1 do {n}!")
            except ValueError:
                print("BŁĄD: Wpisz dwie liczby oddzielone spacją.")

    # 3. WYBÓR SCHEMATU KODOWANIA
    print("\n--- WYBIERZ SCHEMAT KODOWANIA ---")
    print("1. Format z wykładu (Zbiory V i E, system binarny, nawiasy)")
    print("2. Macierz sąsiedztwa (Zapis w postaci macierzy bitów)")
    wybor = input("Wybór (1/2): ")

    if wybor == "1":
        # Format 1: Wykładowy
        v_str = "(" + ",".join([f"[{to_bin(i)}]" for i in range(1, n + 1)]) + ")"
        e_str = "(" + ",".join([f"([{to_bin(u)}],[{to_bin(v)}])" for u, v in raw_edges]) + ")"
        final_chain = f"({v_str},{e_str})"
        format_name = "Format Wykładowy"
        
    else:
        # Format 2: Macierz Sąsiedztwa
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        # Wypełniamy macierz dla grafu nieskierowanego
        for u, v in raw_edges:
            matrix[u-1][v-1] = 1
            matrix[v-1][u-1] = 1 
            
        rows_str = ["".join(map(str, row)) for row in matrix]
        final_chain = f"M=({n},[" + ",".join(rows_str) + "])"
        format_name = "Macierz Sąsiedztwa"

    print(f"\n--- WYGENEROWANY ŁAŃCUCH ZNAKÓW ({format_name}) ---")
    print(final_chain)
    return final_chain

def decode_instance(chain):
    print("\n--- ODCZYT INSTANCJI Z ŁAŃCUCHA (DEKODOWANIE) ---")
    chain = chain.strip() # Usunięcie ewentualnych spacji
    
    try:
        # SPRAWDZENIE FORMATU: MACIERZ SĄSIEDZTWA
        if chain.startswith("M="):
            print("Rozpoznano format: Macierz Sąsiedztwa")
            match = re.search(r'M=\((\d+),\[(.*?)\]\)', chain)
            if not match: raise ValueError("Niepoprawna składnia macierzy.")
            
            n = int(match.group(1))
            rows = match.group(2).split(',')
            
            if len(rows) != n:
                raise ValueError(f"Oczekiwano {n} wierszy, otrzymano {len(rows)}.")
            
            vertices = list(range(1, n + 1))
            edges = []
            
            # Odczytujemy krawędzie (tylko nad przekątną)
            for i in range(n):
                for j in range(i + 1, n):
                    if rows[i][j] == '1':
                        edges.append((i + 1, j + 1))
            v_numbers = vertices

        # SPRAWDZENIE FORMATU: WYKŁADOWY (zaczyna się od nawiasu)
        elif chain.startswith("("):
            print("Rozpoznano format: Zbiory V i E (Wykładowy)")
            v_match = re.search(r'^\(\((.*?)\),', chain)
            if not v_match: raise ValueError("Niepoprawny format zbioru V.")
            
            v_part = v_match.group(1)
            v_numbers = [from_bin(b) for b in re.findall(r'\[([01]+)\]', v_part)]
            
            e_match = re.search(r',(\(.*?\)\))$', chain)
            if not e_match: raise ValueError("Niepoprawny format zbioru E.")
                
            e_part = e_match.group(1)
            e_pairs_raw = re.findall(r'\(\[([01]+)\],\[([01]+)\]\)', e_part)
            edges = [(from_bin(u), from_bin(v)) for u, v in e_pairs_raw]
        
        else:
            raise ValueError("Nierozpoznany format łańcucha wejściowego.")

        # PODSUMOWANIE DLA OBU FORMATÓW
        print(f"\nWynik odkodowania:")
        print(f" -> Liczba wierzchołków: {len(v_numbers)}")
        print(f" -> Wierzchołki V: {v_numbers}")
        print(f" -> Liczba krawędzi: {len(edges)}")
        print(f" -> Krawędzie E: {edges}")
        
        print("\nWeryfikacja instancji (Problem GT11: Partition into Triangles):")
        if len(v_numbers) % 3 == 0 and len(v_numbers) > 0:
            q = len(v_numbers) // 3
            print(f" -> SUKCES: Poprawna instancja! (Liczba wierzchołków to wielokrotność 3, q={q})")
        else:
            print(" -> UWAGA: Niewłaściwa instancja (V nie jest wielokrotnością 3).")
            
    except Exception as e:
        print(f"BŁĄD DEKODOWANIA: Łańcuch jest uszkodzony. ({e})")

def menu():
    last_chain = ""
    while True:
        print("1. Stwórz nową instancję i zakoduj do łańcucha")
        print("2. Dekoduj istniejący łańcuch znaków")
        print("3. Wyjście")
        
        wybor = input("Wybierz opcję (1-3): ")
        
        if wybor == "1":
            last_chain = encode_instance()
        elif wybor == "2":
            if last_chain:
                print(f"Sugestia (ostatni kod): {last_chain}")
            s = input("Wklej łańcuch do zdekodowania: ")
            decode_instance(s)
        elif wybor == "3":
            print("Zamykanie programu...")
            break
        else:
            print("Niepoprawny wybór.")

if __name__ == "__main__":
    menu()