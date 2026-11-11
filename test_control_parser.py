# MiniTAC Compiler
# Control Flow Parser Test


from lexer import tokenize
from parser import Parser


# =====================================================
# SOURCE CODE
# =====================================================

source = """
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


print("=" * 60)
print("TOKENS")
print("=" * 60)

for token in tokens:

    print(token)


# =====================================================
# PARSING
# =====================================================

parser = Parser(tokens)

ast = parser.parse_program()


# =====================================================
# AST
# =====================================================

print("=" * 60)
print("ABSTRACT SYNTAX TREE")
print("=" * 60)

print(ast)


print("=" * 60)
print("PARSER TEST COMPLETED")
print("=" * 60)