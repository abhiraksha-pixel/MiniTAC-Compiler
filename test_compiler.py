# MiniTAC Compiler
# Complete Compiler Pipeline Test


from compiler import Compiler


# =====================================================
# SOURCE CODE
# =====================================================

source = """
a = 10 + 20 * 3;

b = a + 0;

c = b * 1;

if (c > 20) {
    d = c + 5;
}
else {
    d = 0;
}

while (d < 50) {
    d = d + 1;
}
"""


print("=" * 60)
print("MINITAC COMPILER")
print("=" * 60)

print()
print("SOURCE CODE")
print("-----------")

print(source)


# =====================================================
# COMPILE
# =====================================================

compiler = Compiler(source)

final_tac = compiler.compile()

results = compiler.get_results()


# =====================================================
# ORIGINAL TAC
# =====================================================

print("=" * 60)
print("ORIGINAL THREE-ADDRESS CODE")
print("=" * 60)

for instruction in results["tac"]:

    print(instruction)


# =====================================================
# OPTIMIZED TAC
# =====================================================

print("=" * 60)
print("FINAL OPTIMIZED THREE-ADDRESS CODE")
print("=" * 60)

for instruction in final_tac:

    print(instruction)


# =====================================================
# OPTIMIZATION STATISTICS
# =====================================================

stats = results[
    "optimizer_statistics"
]


print("=" * 60)
print("OPTIMIZATION STATISTICS")
print("=" * 60)

print(
    "Constant Folding             : "
    f"{stats['constant_folding']}"
)

print(
    "Constant Propagation         : "
    f"{stats['constant_propagation']}"
)

print(
    "Algebraic Simplification     : "
    f"{stats['algebraic_simplification']}"
)

print(
    "Copy Propagation             : "
    f"{stats['copy_propagation']}"
)

print(
    "Common Subexpression Elim.   : "
    f"{stats['common_subexpression_elimination']}"
)

print(
    "Dead Code Elimination        : "
    f"{stats['dead_code_elimination']}"
)

print(
    "Liveness-Based DCE Removed   : "
    f"{results['dce_removed']}"
)


# =====================================================
# CFG STATISTICS
# =====================================================

cfg = results["cfg"]


print("=" * 60)
print("CONTROL FLOW GRAPH STATISTICS")
print("=" * 60)

print(
    "Basic blocks : "
    f"{len(cfg.blocks)}"
)

print(
    "CFG edges    : "
    f"{sum(len(block.successors) for block in cfg.blocks)}"
)


# =====================================================
# INSTRUCTION REDUCTION
# =====================================================

before = len(
    results["tac"]
)

after = len(
    results["optimized_tac"]
)


print("=" * 60)
print("COMPILATION SUMMARY")
print("=" * 60)

print(
    "Instructions before optimization : "
    f"{before}"
)

print(
    "Instructions after optimization  : "
    f"{after}"
)

if before > 0:

    reduction = (
        (before - after)
        / before
    ) * 100

    print(
        "Instruction reduction            : "
        f"{reduction:.2f}%"
    )


print("=" * 60)
print("COMPILER PIPELINE COMPLETED")
print("=" * 60)