# Test the lexer with control-flow tokens


from lexer import tokenize


# =====================================================
# TEST PROGRAM
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
# TOKENIZATION
# =====================================================

tokens = tokenize(source)


print("=" * 60)
print("TOKENS")
print("=" * 60)


for token in tokens:

    print(token)


print("=" * 60)
print("LEXER TEST COMPLETED")
print("=" * 60)