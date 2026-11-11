# Test program for the MiniTAC Parser

from lexer import tokenize
from parser import Parser


source = "a = 10 + 20 * 3;"

print("Source Code:")
print(source)


# Step 1: Lexical Analysis
tokens = tokenize(source)

print("\nTokens:")
for token in tokens:
    print(token)


# Step 2: Parsing
parser = Parser(tokens)

ast = parser.parse_program()

print("\nAST:")
print(ast)
