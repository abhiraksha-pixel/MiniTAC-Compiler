# MiniTAC Compiler
# Lexer Test Cases

from lexer import tokenize


def run_test(source):
    print("=" * 50)
    print("Source:")
    print(source)

    try:
        tokens = tokenize(source)

        print("\nTokens:")
        for token in tokens:
            print(token)

    except SyntaxError as error:
        print("\nLexer Error:")
        print(error)


# -----------------------------------------
# TEST 1: Basic arithmetic
# -----------------------------------------

run_test("a = 10 + 20 * 3;")


# -----------------------------------------
# TEST 2: Multiple statements
# -----------------------------------------

run_test("""
x = 25;
y = x + 10;
""")


# -----------------------------------------
# TEST 3: Parentheses
# -----------------------------------------

run_test("result = (10 + 5) * 2;")


# -----------------------------------------
# TEST 4: Invalid character
# -----------------------------------------

