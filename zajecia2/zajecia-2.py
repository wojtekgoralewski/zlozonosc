import json

class TuringMachine:
    def __init__(self, config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        self.states = set(config["stany"])
        self.symbols = set(config["symbole"])
        
        self.transitions = {
            (t[0], t[1]): (t[2], t[3], t[4]) for t in config["przejscia"]
        }
        
        self.tape = list(config["tasma"]) if config["tasma"] else ["B"]
        self.state = config["stan_startowy"]
        self.accept_state = config["stan_akceptujacy"]
        self.reject_state = config["stan_odrzucajacy"]
        self.head = 0
        self.blank = "B"

    def display(self, step):
        print(f"Krok: {step} | Stan: {self.state}")
        tape_str = "".join(self.tape)
        print(f"Taśma:  {tape_str}")
        print("        " + " " * self.head + "^")
        print("-" * 30)

    def run(self, interactive=True):
        step = 0
        while self.state not in [self.accept_state, self.reject_state]:
            self.display(step)
            
            if interactive:
                input("Naciśnij Enter...")
            
            current_char = self.tape[self.head]
            action = self.transitions.get((self.state, current_char))
            
            if not action:
                self.state = self.reject_state
                break
                
            new_state, new_char, direction = action
            
            self.tape[self.head] = new_char
            self.state = new_state
            
            if direction == 'R':
                self.head += 1
                if self.head == len(self.tape):
                    self.tape.append(self.blank)
            elif direction == 'L':
                if self.head > 0:
                    self.head -= 1
                else:
                    self.tape.insert(0, self.blank)
            
            step += 1

        self.display(step)
        if self.state == self.accept_state:
            print("Palindrom Poprawny")
        else:
            print("Odrzucenie")

if __name__ == "__main__":
    mt = TuringMachine('input.json')
    mt.run(interactive=True)