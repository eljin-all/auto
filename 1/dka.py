import sys

class DFA:
    TOTAL_STATES = 5
    ALPHABET_CHARACTERS = 2
    Q0, Q1, Q2, Q3, Q4 = range(5)
    ALPHABET = ['a', 'b']
    ACCEPTED_STATES = {Q0, Q1, Q2, Q3}
    TRANSITION_TABLE = []

    @classmethod
    def setup_transitions(cls):
        cls.TRANSITION_TABLE = [[0] * cls.ALPHABET_CHARACTERS for _ in range(cls.TOTAL_STATES)]

        cls.TRANSITION_TABLE[cls.Q0][0] = cls.Q1
        cls.TRANSITION_TABLE[cls.Q0][1] = cls.Q0

        cls.TRANSITION_TABLE[cls.Q1][0] = cls.Q2
        cls.TRANSITION_TABLE[cls.Q1][1] = cls.Q1

        cls.TRANSITION_TABLE[cls.Q2][0] = cls.Q3
        cls.TRANSITION_TABLE[cls.Q2][1] = cls.Q2

        cls.TRANSITION_TABLE[cls.Q3][0] = cls.Q4
        cls.TRANSITION_TABLE[cls.Q3][1] = cls.Q3

        cls.TRANSITION_TABLE[cls.Q4][0] = cls.Q4
        cls.TRANSITION_TABLE[cls.Q4][1] = cls.Q4

    def __init__(self):
        self.current_state = self.Q0

    def reset(self):
        self.current_state = self.Q0

    def step(self, symbol: str) -> bool:
        pos = -1
        for i in range(self.ALPHABET_CHARACTERS):
            if symbol == self.ALPHABET[i]:
                pos = i
                break
        
        if pos == -1:
            return False
        
        self.current_state = self.TRANSITION_TABLE[self.current_state][pos]
        return True

    def is_accepted(self) -> bool:
        return self.current_state in self.ACCEPTED_STATES


def main():
    DFA.setup_transitions()
    dfa = DFA()

    print("ДКА: Число символов 'a' <= 3 в алфавите {a, b")
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

            dfa.reset()
            valid = True

            for ch in line:
                if not dfa.step(ch):
                    valid = False
                    break

            if valid and dfa.is_accepted():
                print(f"'{line}' -> Accept")
            else:
                print(f"'{line}' -> Reject")

        except (KeyboardInterrupt, EOFError):
            break


if __name__ == "__main__":
    main()