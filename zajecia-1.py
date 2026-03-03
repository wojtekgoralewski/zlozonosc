"""[GT11] PARTITION INTO TRIANGLES

INSTANCE: Graph G=(V,E), with V=3q for some integer q.

QUESTION: Can the vertices of G be partitioned into q disjoint sets

VV2..,V, each containing exactly 3 vertices, such that for each

V={u,V, w), 1<i<4, all three of the edges {u,v), (u₁, w,), and {v,, w,} belong

to E?"""


import re

def to_bin(n):
    """Zamienia liczbę na reprezentację binarną (rozsądny schemat kodowania)."""
    return bin(n)[2:]

def from_bin(b):
    """Zamienia ciąg binarny z powrotem na liczbę dziesiętną."""
    return int(b, 2)

def encode_instance():
    print("\n--- TWORZENIE INSTANCJI (KODOWANIE) ---")
    
    # 1. Walidacja V = 3q
    while True:
        try:
            n = int(input("Podaj liczbę wierzchołków (musi być podzielna przez 3, np. 3, 6, 9): "))
            if n > 0 and n % 3 == 0:
                break
            print("BŁĄD: Liczba wierzchołków musi być dodatnią wielokrotnością 3 (zgodnie z V=3q).")
        except ValueError:
            print("BŁĄD: Wprowadź poprawną liczbę całkowitą.")

    try:
        m = int(input("Podaj liczbę krawędzi: "))
    except ValueError:
        m = 0

    # 2. Budowanie zbioru wierzchołków V: ([1],[10],[11])
    v_elements = [f"[{to_bin(i)}]" for i in range(1, n + 1)]
    v_string = "(" + ",".join(v_elements) + ")"
    
    # 3. Budowanie zbioru krawędzi E z walidacją zakresu
    e_elements = []
    print(f"Wprowadź krawędzie (wierzchołki od 1 do {n}):")
    for i in range(m):
        while True:
            try:
                line = input(f"Krawędź {i+1}/{m} (np. '1 2'): ").split()
                u, v = int(line[0]), int(line[1])
                
                if 1 <= u <= n and 1 <= v <= n:
                    # Kodowanie krawędzi jako ([u_bin],[v_bin])
                    e_elements.append(f"([{to_bin(u)}],[{to_bin(v)}])")
                    break
                else:
                    print(f"BŁĄD: Wierzchołki muszą być w zakresie od 1 do {n}!")
            except (ValueError, IndexError):
                print("BŁĄD: Wpisz dwie liczby oddzielone spacją.")
    
    e_string = "(" + ",".join(e_elements) + ")"
    
    # 4. Finalny łańcuch (V, E)
    final_chain = f"({v_string},{e_string})"
    
    print("\n--- WYGENEROWANY ŁAŃCUCH ZNAKÓW ---")
    print(final_chain)
    return final_chain

def decode_instance(chain):
    print("\n--- ODCZYT INSTANCJI Z ŁAŃCUCHA (DEKODOWANIE) ---")
    try:
        # Wyciąganie części V (pierwszy duży blok w nawiasach)
        # Szukamy wzorca: ^((v1,v2,...), (e1,e2,...))
        v_match = re.search(r'^\(\((.*?)\),', chain)
        if not v_match:
            raise ValueError("Niepoprawny format zbioru wierzchołków.")
        
        v_part = v_match.group(1)
        v_numbers = [from_bin(b) for b in re.findall(r'\[([01]+)\]', v_part)]
        
        # Wyciąganie części E
        e_match = re.search(r',(\(.*?\))\)$', chain)
        if not e_match:
            raise ValueError("Niepoprawny format zbioru krawędzi.")
            
        e_part = e_match.group(1)
        e_pairs_raw = re.findall(r'\(\[([01]+)\],\[([01]+)\]\)', e_part)
        edges = [(from_bin(u), from_bin(v)) for u, v in e_pairs_raw]
        
        # Wypisywanie wyników
        print(f"Liczba wierzchołków: {len(v_numbers)}")
        print(f"Wierzchołki V: {v_numbers}")
        print(f"Liczba krawędzi: {len(edges)}")
        print(f"Krawędzie E: {edges}")
        
        q = len(v_numbers) // 3
        print(f"Zadanie: Czy można podzielić te wierzchołki na {q} rozłącznych trójkątów?")
        
    except Exception as e:
        print(f"BŁĄD DEKODOWANIA: Łańcuch jest uszkodzony lub ma zły format. ({e})")

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