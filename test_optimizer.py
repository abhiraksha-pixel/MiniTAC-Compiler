# MiniTAC Compiler
# Optimizer Test with Statistics


from lexer import tokenize
from parser import Parser
from tac import TACGenerator
from optimizer import Optimizer


# =====================================================
# SOURCE PROGRAM
# =====================================================

source = """
a = x + y;
b = x + y;
c = a * 2;
d = x + y;
"""


print("=" * 60)
print("SOURCE CODE")
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


print("=" * 60)
print("UNOPTIMIZED THREE-ADDRESS CODE")
print("=" * 60)

for instruction in tac:

    print(instruction)


# =====================================================
# OPTIMIZATION
# =====================================================

optimizer = Optimizer(tac)

optimized_tac = optimizer.optimize()


print("=" * 60)
print("OPTIMIZED THREE-ADDRESS CODE")
print("=" * 60)

for instruction in optimized_tac:

    print(instruction)


# =====================================================
# OPTIMIZATION STATISTICS
# =====================================================

statistics = optimizer.get_statistics()


print("=" * 60)
print("OPTIMIZATION REPORT")
print("=" * 60)


print(
    f"Constant Folding             : "
    f"{statistics['constant_folding']}"
)

print(
    f"Constant Propagation         : "
    f"{statistics['constant_propagation']}"
)

print(
    f"Algebraic Simplification     : "
    f"{statistics['algebraic_simplification']}"
)

print(
    f"Copy Propagation             : "
    f"{statistics['copy_propagation']}"
)

print(
    f"Common Subexpression Elim.   : "
    f"{statistics['common_subexpression_elimination']}"
)

print(
    f"Dead Code Elimination        : "
    f"{statistics['dead_code_elimination']}"
)


# =====================================================
# INSTRUCTION REDUCTION
# =====================================================

print("=" * 60)
print("OPTIMIZATION SUMMARY")
print("=" * 60)


before = len(tac)

after = len(optimized_tac)


print(
    f"Instructions before optimization : "
    f"{before}"
)

print(
    f"Instructions after optimization  : "
    f"{after}"
)


if before > 0:

    reduction = (
        (before - after)
        / before
    ) * 100

    print(
        f"Instruction reduction            : "
        f"{reduction:.2f}%"
    )