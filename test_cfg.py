# MiniTAC Compiler
# Control Flow Graph Test


from lexer import tokenize
from parser import Parser
from tac import TACGenerator
from cfg import ControlFlowGraph


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
print("SOURCE CODE")
print("=" * 60)

print(source)


# =====================================================
# LEXER
# =====================================================

tokens = tokenize(source)


# =====================================================
# PARSER
# =====================================================

parser = Parser(tokens)

ast = parser.parse_program()


# =====================================================
# TAC GENERATION
# =====================================================

generator = TACGenerator()

tac = generator.generate(ast)


print("=" * 60)
print("THREE-ADDRESS CODE")
print("=" * 60)

for instruction in tac:

    print(instruction)


# =====================================================
# BUILD CFG
# =====================================================

cfg = ControlFlowGraph(tac)

cfg.build()


# =====================================================
# DISPLAY BASIC BLOCKS
# =====================================================

print()
print("=" * 60)
print("CONTROL FLOW GRAPH")
print("=" * 60)

cfg.display()


# =====================================================
# SUMMARY
# =====================================================

print("=" * 60)
print("CFG SUMMARY")
print("=" * 60)

print(
    f"Number of basic blocks: "
    f"{len(cfg.blocks)}"
)

print(
    f"Number of CFG edges: "
    f"{sum(len(block.successors) for block in cfg.blocks)}"
)

print("=" * 60)
print("CFG TEST COMPLETED")
print("=" * 60)