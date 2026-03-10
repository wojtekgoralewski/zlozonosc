import json

class TwoTapeTuringMachineConfigured:
    def __init__(self, config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        self.states = set(config["stany"])
        self.symbols = set(config["symbole"])
        
        self.transitions = {
            (t[0], t[1], t[2]): (t[3], t[4], t[5], t[6], t[7]) for t in config["przejscia"]
        }
        
        self.tape1 = list(config["tasma"]) if config["tasma"] else ["B"]
        self.tape2 = ["B"]
        
        self.head1 = 0
        self.head2 = 0
        
        self.state = config["stan_startowy"]
        self.accept_state = config["stan_akceptujacy"]
        self.reject_state = config["stan_odrzucajacy"]
        self.step_count = 0

    def display(self):
        print(f"2-Tasmowa")
        print(f"Krok: {self.step_count} | Stan: {self.state}")
        
        t1_str = "".join(self.tape1)
        print(f"\nT1: {t1_str}")
        print("    " + " " * self.head1 + "^")
        
        t2_str = "".join(self.tape2)
        print(f"T2: {t2_str}")
        print("    " + " " * self.head2 + "^")
        print("-" * 35)

    def move_head(self, tape_num, direction):
        tape = self.tape1 if tape_num == 1 else self.tape2
        head = self.head1 if tape_num == 1 else self.head2
        
        if direction == 'R':
            head += 1
            if head == len(tape):
                tape.append('B')
        elif direction == 'L':
            if head > 0:
                head -= 1
            else:
                tape.insert(0, 'B')
                # Jeśli wstawiamy element na początek, musimy przesunąć pozycję głowicy o 1
                
        if tape_num == 1: self.head1 = head
        else: self.head2 = head

    def run(self, interactive=True):
        while self.state not in [self.accept_state, self.reject_state]:
            self.display()
            if interactive:
                input("Naciśnij Enter...")
            
            char1 = self.tape1[self.head1]
            char2 = self.tape2[self.head2]
            
            action = self.transitions.get((self.state, char1, char2))
            
            if not action:
                self.state = self.reject_state
                break
                
            new_state, write1, write2, dir1, dir2 = action
            
            self.tape1[self.head1] = write1
            self.tape2[self.head2] = write2
            self.state = new_state
            
            if dir1 != 'S': self.move_head(1, dir1)
            if dir2 != 'S': self.move_head(2, dir2)
            
            self.step_count += 1

        self.display()
        if self.state == self.accept_state:
            print("Palindrom poprawny")
        else:
            print("Błąd sprawdzenia")

# --- URUCHOMIENIE ---
if __name__ == "__main__":
    mt = TwoTapeTuringMachineConfigured('input2.json')
    mt.run(interactive=True)