import sys

class NFA:
    TOTAL_STATES = 5
    ALPHABET_CHARACTERS = 3
    Q0, Q1, Q2, Q3, Q4 = range(5)
    ALPHABET = ['1', '2', '3']
    ACCEPTED_STATES = {Q4}
    TRANSITION_TABLE = []

    @classmethod
    def setup_transitions(cls):
        cls.TRANSITION_TABLE = [[set() for _ in range(cls.ALPHABET_CHARACTERS)] for _ in range(cls.TOTAL_STATES)]

        cls.TRANSITION_TABLE[cls.Q0][0] = {cls.Q0, cls.Q1}
        cls.TRANSITION_TABLE[cls.Q0][1] = {cls.Q0, cls.Q2}
        cls.TRANSITION_TABLE[cls.Q0][2] = {cls.Q0, cls.Q3}

        cls.TRANSITION_TABLE[cls.Q1][0] = {cls.Q1, cls.Q4}
        cls.TRANSITION_TABLE[cls.Q1][1] = {cls.Q1}
        cls.TRANSITION_TABLE[cls.Q1][2] = {cls.Q1}

        cls.TRANSITION_TABLE[cls.Q2][0] = {cls.Q2}
        cls.TRANSITION_TABLE[cls.Q2][1] = {cls.Q2, cls.Q4}
        cls.TRANSITION_TABLE[cls.Q2][2] = {cls.Q2}

        cls.TRANSITION_TABLE[cls.Q3][0] = {cls.Q3}
        cls.TRANSITION_TABLE[cls.Q3][1] = {cls.Q3}
        cls.TRANSITION_TABLE[cls.Q3][2] = {cls.Q3, cls.Q4}

    def __init__(self):
        self.current_states = {self.Q0}

    def reset(self):
        self.current_states = {self.Q0}

    def step(self, symbol: str) -> bool:
        pos = -1
        for i in range(self.ALPHABET_CHARACTERS):
            if symbol == self.ALPHABET[i]:
                pos = i
                break
        
        if pos == -1:
            return False
        
        next_states = set()
        for state in self.current_states:
            targets = self.TRANSITION_TABLE[state][pos]
            for target in targets:
                next_states.add(target)
                
        self.current_states = next_states
        return True

    def is_accepted(self) -> bool:
        for st in self.current_states:
            if st in self.ACCEPTED_STATES:
                return True
        return False


def main():
    NFA.setup_transitions()
    nfa = NFA()

    print("НКА: Последний символ уже встречался ранее в {1, 2, 3}")
    print("Введите строку (или 'exit' для выхода):")

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            if len(line) > 0 and line[-1] == '\n':
                line = line[:-1]
            if len(line) > 0 and line[-1] == '\r':
                line = line[:-1]

            if line == "exit":
                break

            nfa.reset()
            valid = True

            for ch in line:
                if not nfa.step(ch):
                    valid = False
                    break

            if valid and nfa.is_accepted():
                print(f"'{line}' -> Accept")
            else:
                print(f"'{line}' -> Reject")

        except (KeyboardInterrupt, EOFError):
            break


if __name__ == "__main__":
    main()