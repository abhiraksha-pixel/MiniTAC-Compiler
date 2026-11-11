# MiniTAC Compiler
# Automated Dead Code Elimination Tests
#
# Run with:
# python -m pytest tests/test_dead_code_elimination.py -v


from lexer import tokenize
from parser import Parser
from tac import TACGenerator
from cfg import ControlFlowGraph
from dataflow import LivenessAnalyzer
from dce import DeadCodeEliminator


def generate_tac(source):
    """
    Convert source code into Three-Address Code.
    """

    tokens = tokenize(source)

    parser = Parser(tokens)

    ast = parser.parse_program()

    generator = TACGenerator()

    return generator.generate(ast)


def run_dce(tac):
    """
    Build CFG, perform liveness analysis,
    then run Dead Code Elimination.
    """

    cfg = ControlFlowGraph(tac)

    cfg.build()

    analyzer = LivenessAnalyzer(cfg)

    analyzer.analyze()

    dce = DeadCodeEliminator(
        cfg,
        analyzer
    )

    optimized_blocks = dce.eliminate()

    optimized_tac = dce.get_optimized_tac(
        optimized_blocks
    )

    return optimized_tac, dce


def run_dce_from_source(source):
    """
    Complete source → TAC → CFG → Liveness → DCE pipeline.
    """

    tac = generate_tac(source)

    optimized_tac, dce = run_dce(tac)

    return tac, optimized_tac, dce


# =====================================================
# DEAD TEMPORARY IS REMOVED
# =====================================================

def test_dead_temporary_is_removed():

    tac = [
        "t1 = 10",
        "a = 5"
    ]

    optimized, dce = run_dce(tac)

    assert "t1 = 10" not in optimized

    assert "a = 5" in optimized

    assert dce.get_removed_count() == 1


# =====================================================
# USED TEMPORARY IS PRESERVED
# =====================================================

def test_used_temporary_is_preserved():

    tac = [
        "t1 = 10",
        "a = t1"
    ]

    optimized, dce = run_dce(tac)

    # t1 is required by a.

    assert "t1 = 10" in optimized

    assert "a = t1" in optimized

    assert dce.get_removed_count() == 0


# =====================================================
# MULTIPLE DEAD TEMPORARIES
# =====================================================

def test_multiple_dead_temporaries_are_removed():

    tac = [
        "t1 = 10",
        "t2 = 20",
        "t3 = t1 + t2",
        "a = 5"
    ]

    optimized, dce = run_dce(tac)

    # All temporary calculations are unused.

    assert "t1 = 10" not in optimized

    assert "t2 = 20" not in optimized

    assert "t3 = t1 + t2" not in optimized

    assert "a = 5" in optimized

    assert dce.get_removed_count() == 3


# =====================================================
# DEAD TEMPORARY CHAIN
# =====================================================

def test_dead_temporary_chain_is_removed():

    tac = [
        "a = 10",
        "t1 = a + 20",
        "t2 = t1 * 2",
        "t3 = t2 + 5",
        "b = 100"
    ]

    optimized, dce = run_dce(tac)

    # None of the temporary values reaches
    # a useful assignment.

    assert "t1 = a + 20" not in optimized

    assert "t2 = t1 * 2" not in optimized

    assert "t3 = t2 + 5" not in optimized

    assert "a = 10" in optimized

    assert "b = 100" in optimized

    assert dce.get_removed_count() == 3


# =====================================================
# SOURCE CODE DCE
# =====================================================



# =====================================================
# CONTROL FLOW IS PRESERVED
# =====================================================

def test_control_flow_is_preserved():

    tac = [
        "a = 10",
        "if a > 5 goto L1",
        "goto L2",
        "L1:",
        "t1 = 20",
        "b = t1",
        "goto L3",
        "L2:",
        "b = 0",
        "L3:"
    ]

    optimized, dce = run_dce(tac)

    # Control-flow instructions must remain.

    assert "if a > 5 goto L1" in optimized

    assert "goto L2" in optimized

    assert "L1:" in optimized

    assert "L2:" in optimized

    assert "L3:" in optimized


# =====================================================
# LOOP IS PRESERVED
# =====================================================

def test_loop_is_preserved():

    tac = [
        "L1:",
        "if b < 20 goto L2",
        "goto L3",
        "L2:",
        "t1 = b + 1",
        "b = t1",
        "goto L1",
        "L3:"
    ]

    optimized, dce = run_dce(tac)

    # Loop condition remains.

    assert "if b < 20 goto L2" in optimized

    # Loop body remains because b is used
    # by the next loop condition.

    assert "b = t1" in optimized

    # Back edge remains.

    assert "goto L1" in optimized

    # Exit remains.

    assert "L3:" in optimized


# =====================================================
# NO DEAD CODE
# =====================================================

def test_no_dead_code():

    tac = [
        "t1 = 10",
        "a = t1",
        "t2 = a + 5",
        "b = t2"
    ]

    optimized, dce = run_dce(tac)

    # Every temporary is required.

    assert "t1 = 10" in optimized

    assert "a = t1" in optimized

    assert "t2 = a + 5" in optimized

    assert "b = t2" in optimized

    assert dce.get_removed_count() == 0