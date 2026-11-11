# Test program for TAC generation

from lexer import tokenize
from parser import Parser
from tac import TACGenerator


# -----------------------------------------
# Source program
# -----------------------------------------

source = "a = 10 + 20 * 3;"


print("SOURCE CODE")
print("-----------")
print(source)


# -----------------------------------------
# Phase 1: Lexical Analysis
# -----------------------------------------

tokens = tokenize(source)


# -----------------------------------------
# Phase 2: Parsing
# -----------------------------------------

parser = Parser(tokens)

ast = parser.parse_program()


# -----------------------------------------
# Phase 3: TAC Generation
# -----------------------------------------

generator = TACGenerator()

tac = generator.generate(ast)


# -----------------------------------------
# Display TAC
# -----------------------------------------

print("\nTHREE-ADDRESS CODE")
print("------------------")

for instruction in tac:
    print(instruction)