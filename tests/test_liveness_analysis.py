# MiniTAC Compiler
# Automated Liveness / Data Flow Analysis Tests
#
# Run with:
# python -m pytest tests/test_liveness_analysis.py -v


from lexer import tokenize
from parser import Parser
from tac import TACGenerator
from cfg import ControlFlowGraph
from dataflow import LivenessAnalyzer


def generate_tac(source):
    """
    Convert source code into Three-Address Code.
    """

    tokens = tokenize(source)

    parser = Parser(tokens)

    ast = parser.parse_program()

    generator = TACGenerator()

    return generator.generate(ast)


def analyze_source(source):
    """
    Generate TAC, build CFG and perform liveness analysis.
    """

    tac = generate_tac(source)

    cfg = ControlFlowGraph(tac)

    cfg.build()

    analyzer = LivenessAnalyzer(cfg)

    live_in, live_out = analyzer.analyze()

    return tac, cfg, analyzer, live_in, live_out


# =====================================================
# USE / DEF ANALYSIS
# =====================================================

def test_use_def_analysis():

    source = """
    b = x + 5;
    """

    tac, cfg, analyzer, live_in, live_out = analyze_source(source)

    assert len(cfg.blocks) >= 1

    target_block = cfg.blocks[0]

    block_id = target_block.block_id

    # x is used before being defined in this block.

    assert "x" in analyzer.uses[block_id]

    # b is defined by the assignment.

    assert "b" in analyzer.definitions[block_id]


# =====================================================
# LIVE VARIABLE BEFORE USE
# =====================================================

def test_variable_is_live_before_use():

    source = """
    b = x + 5;
    """

    tac, cfg, analyzer, live_in, live_out = analyze_source(source)

    block = cfg.blocks[0]

    block_id = block.block_id

    # x is required before the block executes.

    assert "x" in live_in[block_id]


# =====================================================
# CONSTANT-ONLY ASSIGNMENT
# =====================================================

def test_constant_assignment_has_no_external_use():

    source = """
    a = 10;
    """

    tac, cfg, analyzer, live_in, live_out = analyze_source(source)

    block = cfg.blocks[0]

    block_id = block.block_id

    # No external variable is required.

    assert analyzer.uses[block_id] == set()


# =====================================================
# CONDITIONAL USE
# =====================================================

def test_condition_variables_are_live():

    source = """
    if (x > 10) {
        b = 20;
    }
    else {
        b = 0;
    }
    """

    tac, cfg, analyzer, live_in, live_out = analyze_source(source)

    condition_block = None

    for block in cfg.blocks:

        if any(
            instruction.startswith(
                "if x > 10 goto"
            )
            for instruction in block.instructions
        ):

            condition_block = block

            break

    assert condition_block is not None

    block_id = condition_block.block_id

    # x is not defined before the condition,
    # therefore it is a USE of the block.

    assert "x" in analyzer.uses[block_id]

    # x must be live before the condition.

    assert "x" in live_in[block_id]


# =====================================================
# LOOP VARIABLE LIVENESS
# =====================================================

def test_loop_variable_is_live():

    source = """
    b = 10;

    while (b < 20) {
        b = b + 1;
    }
    """

    tac, cfg, analyzer, live_in, live_out = analyze_source(source)

    condition_block = None

    for block in cfg.blocks:

        if any(
            instruction.startswith(
                "if b < 20 goto"
            )
            for instruction in block.instructions
        ):

            condition_block = block

            break

    assert condition_block is not None

    block_id = condition_block.block_id

    # b is used by the loop condition.

    assert "b" in analyzer.uses[block_id]

    # b must be live before the condition.

    assert "b" in live_in[block_id]


# =====================================================
# LIVE VARIABLE PROPAGATION
# =====================================================

def test_liveness_propagates_between_blocks():

    source = """
    if (x > 5) {
        b = 10;
    }
    else {
        b = 20;
    }

    c = b + 2;
    """

    tac, cfg, analyzer, live_in, live_out = analyze_source(source)

    # Find the block containing c = b + 2.

    use_block = None

    for block in cfg.blocks:

        if any(
            "b + 2" in instruction
            for instruction in block.instructions
        ):

            use_block = block

            break

    assert use_block is not None

    use_block_id = use_block.block_id

    # b is used in this block.

    assert "b" in analyzer.uses[use_block_id]

    # Find predecessors.

    predecessors_found = False

    for block in cfg.blocks:

        if use_block in block.successors:

            predecessors_found = True

            # b must be live after a predecessor.

            assert "b" in live_out[block.block_id]

    assert predecessors_found


# =====================================================
# IN / OUT SETS EXIST
# =====================================================

def test_live_in_and_live_out_sets_exist():

    source = """
    a = 10;
    b = a + 5;
    c = b * 2;
    """

    tac, cfg, analyzer, live_in, live_out = analyze_source(source)

    assert len(live_in) == len(cfg.blocks)

    assert len(live_out) == len(cfg.blocks)

    for block in cfg.blocks:

        assert block.block_id in live_in

        assert block.block_id in live_out

        assert isinstance(
            live_in[block.block_id],
            set
        )

        assert isinstance(
            live_out[block.block_id],
            set
        )


# =====================================================
# ANALYSIS TERMINATES WITH LOOP
# =====================================================

def test_analysis_handles_loop():

    source = """
    i = 0;

    while (i < 10) {
        i = i + 1;
    }
    """

    tac, cfg, analyzer, live_in, live_out = analyze_source(source)

    # Analysis should finish.

    assert len(live_in) == len(cfg.blocks)

    assert len(live_out) == len(cfg.blocks)

    # i should be live somewhere in the loop.

    assert any(
        "i" in values
        for values in live_in.values()
    )