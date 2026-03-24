class RAMMachine:
    def __init__(self):
        self.memory = {}
        self.accumulator = 0
        self.program = []
        self.pc = 0

    def load_program(self, filename):
        self.program = []
        try:
            with open(filename, 'r', encoding="utf-8") as f:
                for line in f:
                    # Usuwanie komentarzy i czyszczenie białych znaków
                    line = line.split("//")[0].strip()
                    if not line: continue
                    parts = line.split()
                    # Obsługa formatu: [numer] INSTRUKCJA [argument]
                    if parts[0].isdigit():
                        instr = parts[1].upper()
                        arg = int(parts[2]) if len(parts) > 2 else None
                    else:
                        instr = parts[0].upper()
                        arg = int(parts[1]) if len(parts) > 1 else None
                    self.program.append((instr, arg))
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku {filename}!")
            exit()

    def run(self, inputs):
        input_ptr = 0
        self.pc = 0
        self.memory = {}
        self.accumulator = 0
        step = 1

        print(f"{'KROK':<5} | {'INSTRUKCJA':<12} | {'AKUMULATOR':<10} | {'REJESTRY'}")
        print("-" * 60)

        while 0 <= self.pc < len(self.program):
            instr, arg = self.program[self.pc]
            
            # Zapamiętujemy instrukcję do wyświetlenia przed zmianą PC
            display_instr = f"{instr} {arg if arg is not None else ''}"
            
            self.pc += 1 

            # Logika instrukcji
            if instr == "READ":
                self.memory[arg] = inputs[input_ptr]
                input_ptr += 1
            elif instr == "LOAD":
                self.accumulator = self.memory.get(arg, 0)
            elif instr == "STORE":
                self.memory[arg] = self.accumulator
            elif instr == "ADD":
                self.accumulator += self.memory.get(arg, 0)
            elif instr == "SUB":
                val = self.memory.get(arg, 0)
                self.accumulator = max(0, self.accumulator - val)
            elif instr == "HALF":
                self.accumulator //= 2
            elif instr == "JZERO":
                if self.accumulator == 0:
                    self.pc = arg - 1
            elif instr == "JGTZ":
                if self.accumulator > 0:
                    self.pc = arg - 1
            elif instr == "WRITE":
                print(f"\n>>> WYJŚCIE: {self.memory.get(arg, 0)}\n")
            elif instr == "HALT":
                print(f"{step:<5} | {display_instr:<12} | {self.accumulator:<10} | {self.memory}")
                break

            # Wypisywanie stanu po każdym kroku
            print(f"{step:<5} | {display_instr:<12} | {self.accumulator:<10} | {self.memory}")
            step += 1

# Uruchomienie
if __name__ == "__main__":
    machine = RAMMachine()
    machine.load_program("zasady.txt")
    
    print("--- Symulator Maszyny RAM ---")
    n1 = int(input("Podaj A: "))
    n2 = int(input("Podaj B: "))
    print()
    
    machine.run([n1, n2])