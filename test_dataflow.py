# MiniTAC Compiler
# Liveness Analysis Test


from lexer import tokenize
from parser import Parser
from tac import TACGenerator
from cfg import ControlFlowGraph
from dataflow import LivenessAnalyzer


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
# TAC
# =====================================================

generator = TACGenerator()

tac = generator.generate(ast)


print("=" * 60)
print("THREE-ADDRESS CODE")
print("=" * 60)

for instruction in tac:

    print(instruction)


# =====================================================
# CFG
# =====================================================

cfg = ControlFlowGraph(tac)

cfg.build()


# =====================================================
# LIVENESS ANALYSIS
# =====================================================

analyzer = LivenessAnalyzer(cfg)

analyzer.analyze()

analyzer.display()


# =====================================================
# SUMMARY
# =====================================================

print()
print("=" * 60)
print("DATA FLOW ANALYSIS COMPLETED")
print("=" * 60)