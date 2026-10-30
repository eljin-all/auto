"""
Практическая работа №5. Часть 2 (Вариант 5).
Синтаксический анализ методом рекурсивного спуска.
Язык: последовательности выражений с разделителем ';'.
Элементы: переменные (1-2 символа), целые константы (10-чные),
          вещественные константы только в экспоненциальной форме.
"""

import sys
import re

# Типы лексем
T_VAR = 'VAR' 
T_INT = 'INT' 
T_FLOAT = 'FLOAT' 
T_ASSIGN = '='
T_PLUS = '+'
T_MINUS = '-'
T_MUL = '*'
T_DIV = '/'
T_LPAREN = '('
T_RPAREN = ')'
T_SEMI = ';'
T_EOF = 'EOF'


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def get_next_token(self) -> Token:
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

        if self.pos >= len(self.text):
            return Token(T_EOF, None)

        ch = self.text[self.pos]

        if ch == '=': self.pos += 1; return Token(T_ASSIGN, '=')
        if ch == '+': self.pos += 1; return Token(T_PLUS, '+')
        if ch == '-': self.pos += 1; return Token(T_MINUS, '-')
        if ch == '*': self.pos += 1; return Token(T_MUL, '*')
        if ch == '/': self.pos += 1; return Token(T_DIV, '/')
        if ch == '(': self.pos += 1; return Token(T_LPAREN, '(')
        if ch == ')': self.pos += 1; return Token(T_RPAREN, ')')
        if ch == ';': self.pos += 1; return Token(T_SEMI, ';')

        if ch.isdigit():
            start = self.pos
            exp_match = re.match(r'^\d+\.\d+[eE][+-]?\d+', self.text[self.pos:])
            if exp_match:
                val = exp_match.group(0)
                self.pos += len(val)
                return Token(T_FLOAT, val)

            float_no_exp = re.match(r'^\d+\.\d+', self.text[self.pos:])
            if float_no_exp:
                raise ValueError(f"Обычный вещественный формат запрещен: {float_no_exp.group(0)}")

            int_match = re.match(r'^\d+', self.text[self.pos:])
            val = int_match.group(0)
            self.pos += len(val)
            return Token(T_INT, val)

        if ch.isalpha():
            start = self.pos
            while self.pos < len(self.text) and (self.text[self.pos].isalnum()):
                self.pos += 1
            ident = self.text[start:self.pos]
            if len(ident) in (1, 2):
                return Token(T_VAR, ident)
            else:
                raise ValueError(f"Длина переменной превышает 2 символа: {ident}")

        raise ValueError(f"Неизвестный символ: {ch}")


class RecursiveDescentParser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, msg="Синтаксическая ошибка"):
        raise SyntaxError(msg)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Ожидался {token_type}, получен {self.current_token.type}")

    def parse_sequence(self):
        self.parse_expr()
        while self.current_token.type == T_SEMI:
            self.eat(T_SEMI)
            if self.current_token.type == T_EOF:
                break
            self.parse_expr()
        if self.current_token.type != T_EOF:
            self.error("Лишние символы в конце входного потока")

    def parse_expr(self):
        if self.current_token.type == T_VAR:
            saved_pos = self.lexer.pos
            saved_token = self.current_token
            var_token = self.current_token
            self.eat(T_VAR)
            if self.current_token.type == T_ASSIGN:
                self.eat(T_ASSIGN)
                self.parse_expr()
                return
            else:
                self.lexer.pos = saved_pos
                self.current_token = saved_token

        self.parse_add()

    def parse_add(self):
        self.parse_term()
        while self.current_token.type in (T_PLUS, T_MINUS):
            self.eat(self.current_token.type)
            self.parse_term()

    def parse_term(self):
        self.parse_factor()
        while self.current_token.type in (T_MUL, T_DIV):
            self.eat(self.current_token.type)
            self.parse_factor()

    def parse_factor(self):
        if self.current_token.type == T_MINUS:
            self.eat(T_MINUS)
            self.parse_factor()
        else:
            self.parse_primary()

    def parse_primary(self):
        token = self.current_token
        if token.type == T_LPAREN:
            self.eat(T_LPAREN)
            self.parse_expr()
            self.eat(T_RPAREN)
        elif token.type == T_VAR:
            self.eat(T_VAR)
        elif token.type == T_INT:
            self.eat(T_INT)
        elif token.type == T_FLOAT:
            self.eat(T_FLOAT)
        else:
            self.error(f"Неожиданный операнд: {token}")


def check_string(s: str) -> str:
    try:
        lexer = Lexer(s)
        parser = RecursiveDescentParser(lexer)
        parser.parse_sequence()
        return "Accepted"
    except Exception:
        return "Rejected"


if __name__ == '__main__':
    test_suite = [
        ("a = 1.5e2"),
        ("x1 = 20 + 3.14e-1; y = -x1 * 2"),
        ("ab = -(c + 4) / 1.0e+3"),
        ("val = 100"),
        ("a = 1.0e2; b = 5; c = a * b"),
        ("a = 1.5"),
        ("var_long = 1.0e2"),
        ("a = 1.5e2 +"), 
        ("a = (b + 2; c = 1"),
        ("a = 1.0e2 ;; b = 2")
    ]

    print(f"{'Тестовая строка':<40} | {'Результат':<10}")
    print("-" * 65)
    for text in test_suite:
        actual = check_string(text)
        print(f"{text:<40} | {actual:<10}")