# MiniTAC Compiler
# Automated Control Flow Graph Tests
#
# Run with:
# python -m pytest tests/test_control_flow_graph.py -v


from lexer import tokenize
from parser import Parser
from tac import TACGenerator
from cfg import ControlFlowGraph


def generate_tac(source):
    """
    Convert source code into TAC.
    """

    tokens = tokenize(source)

    parser = Parser(tokens)

    ast = parser.parse_program()

    generator = TACGenerator()

    return generator.generate(ast)


def build_cfg(source):
    """
    Generate TAC and build the CFG.
    """

    tac = generate_tac(source)

    cfg = ControlFlowGraph(tac)

    # IMPORTANT:
    # ControlFlowGraph() creates an empty graph.
    # build() creates the basic blocks and edges.

    cfg.build()

    return tac, cfg


# =====================================================
# BASIC BLOCK CREATION
# =====================================================

def test_basic_blocks_are_created():

    source = """
    a = 10;

    if (a > 5) {
        b = a + 1;
    }
    else {
        b = 0;
    }
    """

    tac, cfg = build_cfg(source)

    assert len(cfg.blocks) > 1


# =====================================================
# IF / ELSE CFG
# =====================================================

def test_if_else_cfg():

    source = """
    a = 15;

    if (a > 10) {
        b = a + 1;
    }
    else {
        b = 0;
    }
    """

    tac, cfg = build_cfg(source)

    # Conditional jump must exist.

    assert any(
        instruction.startswith(
            "if a > 10 goto"
        )
        for instruction in tac
    )

    # Then branch.

    assert any(
        "a + 1" in instruction
        for instruction in tac
    )

    # Else branch.

    assert "b = 0" in tac

    # Multiple basic blocks are required.

    assert len(cfg.blocks) >= 4


# =====================================================
# WHILE CFG
# =====================================================

def test_while_cfg():

    source = """
    b = 10;

    while (b < 20) {
        b = b + 1;
    }
    """

    tac, cfg = build_cfg(source)

    # Loop condition.

    assert any(
        instruction.startswith(
            "if b < 20 goto"
        )
        for instruction in tac
    )

    # Loop body.

    assert any(
        "b + 1" in instruction
        for instruction in tac
    )

    # There must be a goto.

    assert any(
        instruction.startswith("goto L")
        for instruction in tac
    )

    # A loop requires multiple blocks.

    assert len(cfg.blocks) >= 3


# =====================================================
# IF + WHILE
# =====================================================

def test_if_and_while_cfg():

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

    tac, cfg = build_cfg(source)

    # IF condition.

    assert any(
        instruction.startswith(
            "if a > 10 goto"
        )
        for instruction in tac
    )

    # WHILE condition.

    assert any(
        instruction.startswith(
            "if b < 20 goto"
        )
        for instruction in tac
    )

    # Several basic blocks should exist.

    assert len(cfg.blocks) >= 7


# =====================================================
# CFG EDGES
# =====================================================

def test_cfg_has_edges():

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

    tac, cfg = build_cfg(source)

    # At least one block should have successors.

    has_successor = False

    for block in cfg.blocks:

        if hasattr(block, "successors"):

            if len(block.successors) > 0:

                has_successor = True

                break

    assert has_successor


# =====================================================
# ENTRY BLOCK
# =====================================================

def test_cfg_has_entry_block():

    source = """
    a = 10;
    b = a + 5;
    """

    tac, cfg = build_cfg(source)

    assert len(cfg.blocks) >= 1

    # First block should contain the first TAC instruction.

    first_block = cfg.blocks[0]

    assert "a = 10" in first_block.instructions