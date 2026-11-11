# MiniTAC Compiler
# Control Flow TAC Test


from lexer import tokenize
from parser import Parser
from tac import TACGenerator


# =====================================================
# SOURCE CODE
# =====================================================

source = """
a = 15;

if (a > 10) {
    b = a + 1;
}
else {
    b = 0;
}

while (b < 20) {
    b = b + 1;
}
"""


print("=" * 60)
print("CONTROL FLOW SOURCE CODE")
print("=" * 60)

print(source)


# =====================================================
# LEXICAL ANALYSIS
# =====================================================

tokens = tokenize(source)


# =====================================================
# PARSING
# =====================================================

parser = Parser(tokens)

ast = parser.parse_program()


# =====================================================
# TAC GENERATION
# =====================================================

generator = TACGenerator()

tac = generator.generate(ast)


# =====================================================
# DISPLAY TAC
# =====================================================

print("=" * 60)
print("CONTROL FLOW THREE-ADDRESS CODE")
print("=" * 60)

for instruction in tac:

    print(instruction)


print("=" * 60)
print("TAC TEST COMPLETED")
print("=" * 60)