# MiniTAC Compiler
# Direct Liveness-Based DCE Test


from cfg import ControlFlowGraph
from dataflow import LivenessAnalyzer
from dce import DeadCodeEliminator


# =====================================================
# MANUAL TAC
# =====================================================

tac = [

    "a = 10",

    "t1 = a + 20",

    "t2 = t1 * 2",

    "t3 = 100 + 200",

    "b = a + 5"
]


print("=" * 60)
print("ORIGINAL THREE-ADDRESS CODE")
print("=" * 60)

for instruction in tac:

    print(instruction)


# =====================================================
# CFG
# =====================================================

cfg = ControlFlowGraph(tac)

cfg.build()


# =====================================================
# LIVENESS
# =====================================================

analyzer = LivenessAnalyzer(cfg)

analyzer.analyze()


# =====================================================
# DCE
# =====================================================

dce = DeadCodeEliminator(
    cfg,
    analyzer
)

optimized_blocks = dce.eliminate()

optimized_tac = dce.get_optimized_tac(
    optimized_blocks
)


# =====================================================
# RESULT
# =====================================================

print("=" * 60)
print("OPTIMIZED THREE-ADDRESS CODE")
print("=" * 60)

for instruction in optimized_tac:

    print(instruction)


# =====================================================
# SUMMARY
# =====================================================

print("=" * 60)
print("DCE SUMMARY")
print("=" * 60)

print(
    f"Instructions before : "
    f"{len(tac)}"
)

print(
    f"Instructions after  : "
    f"{len(optimized_tac)}"
)

print(
    f"Instructions removed: "
    f"{dce.get_removed_count()}"
)

print("=" * 60)
print("DCE TEST COMPLETED")
print("=" * 60)