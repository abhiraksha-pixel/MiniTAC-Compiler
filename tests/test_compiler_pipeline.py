# MiniTAC Compiler
# Automated Full Compiler Pipeline Tests
#
# Run with:
# python -m pytest tests/test_compiler_pipeline.py -v


from compiler import Compiler


# =====================================================
# BASIC COMPILATION
# =====================================================

def test_compiler_runs():

    source = """
    a = 10;
    b = a + 5;
    """

    compiler = Compiler(source)

    result = compiler.compile()

    assert result is not None

    assert isinstance(result, list)

    assert len(result) > 0


# =====================================================
# ALL PIPELINE RESULTS ARE AVAILABLE
# =====================================================

def test_compiler_returns_all_results():

    source = """
    a = 10;
    b = a + 5;
    """

    compiler = Compiler(source)

    compiler.compile()

    results = compiler.get_results()

    assert "source" in results

    assert "tokens" in results

    assert "ast" in results

    assert "tac" in results

    assert "optimized_tac" in results

    assert "cfg" in results

    assert "liveness" in results

    assert "optimizer_statistics" in results

    assert "dce_removed" in results


# =====================================================
# LEXER → PARSER → TAC PIPELINE
# =====================================================

def test_frontend_pipeline():

    source = """
    a = 10 + 20 * 3;
    """

    compiler = Compiler(source)

    compiler.compile()

    results = compiler.get_results()

    # Tokens should be generated.

    assert len(results["tokens"]) > 0

    # AST should be generated.

    assert len(results["ast"]) > 0

    # TAC should be generated.

    assert len(results["tac"]) > 0

    # Final TAC should also exist.

    assert len(results["optimized_tac"]) > 0


# =====================================================
# OPTIMIZATION STAGE
# =====================================================

def test_optimizer_is_executed():

    source = """
    a = 10 + 20;
    """

    compiler = Compiler(source)

    compiler.compile()

    results = compiler.get_results()

    statistics = results["optimizer_statistics"]

    assert isinstance(statistics, dict)

    # The optimizer should expose statistics.

    assert len(statistics) > 0


# =====================================================
# CONTROL FLOW PIPELINE
# =====================================================

def test_control_flow_pipeline():

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

    compiler = Compiler(source)

    compiler.compile()

    results = compiler.get_results()

    tac = results["tac"]

    optimized_tac = results["optimized_tac"]

    cfg = results["cfg"]

    # IF condition should exist.

    assert any(
        instruction.startswith(
            "if a > 10 goto"
        )
        for instruction in tac
    )

    # WHILE condition should exist.

    assert any(
        instruction.startswith(
            "if b < 20 goto"
        )
        for instruction in tac
    )

    # CFG must contain basic blocks.

    assert len(cfg.blocks) > 1

    # Final TAC should still contain control flow.

    assert any(
        instruction.startswith("if ")
        for instruction in optimized_tac
    )

    assert any(
        instruction.startswith("goto ")
        for instruction in optimized_tac
    )


# =====================================================
# LIVENESS ANALYSIS IS EXECUTED
# =====================================================

def test_liveness_pipeline():

    source = """
    a = 10;

    b = a + 5;
    """

    compiler = Compiler(source)

    compiler.compile()

    results = compiler.get_results()

    liveness = results["liveness"]

    assert liveness is not None

    assert len(liveness.live_in) == len(
        results["cfg"].blocks
    )

    assert len(liveness.live_out) == len(
        results["cfg"].blocks
    )


# =====================================================
# DCE STAGE IS EXECUTED
# =====================================================

def test_dce_pipeline():

    source = """
    a = 10 + 20 * 3;

    b = a + 0;

    c = b * 1;
    """

    compiler = Compiler(source)

    compiler.compile()

    results = compiler.get_results()

    assert isinstance(
        results["dce_removed"],
        int
    )

    assert results["dce_removed"] >= 0


# =====================================================
# COMPLETE PROGRAM
# =====================================================

def test_complete_compiler_pipeline():

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

    compiler = Compiler(source)

    final_tac = compiler.compile()

    results = compiler.get_results()

    # ---------------------------------------------
    # Frontend
    # ---------------------------------------------

    assert len(results["tokens"]) > 0

    assert len(results["ast"]) > 0

    # ---------------------------------------------
    # TAC
    # ---------------------------------------------

    assert len(results["tac"]) > 0

    # ---------------------------------------------
    # Optimization
    # ---------------------------------------------

    assert len(results["optimized_tac"]) > 0

    # ---------------------------------------------
    # CFG
    # ---------------------------------------------

    assert results["cfg"] is not None

    assert len(
        results["cfg"].blocks
    ) >= 1

    # ---------------------------------------------
    # Liveness
    # ---------------------------------------------

    assert results["liveness"] is not None

    # ---------------------------------------------
    # Final result
    # ---------------------------------------------

    assert final_tac == results["optimized_tac"]


# =====================================================
# COMPILER CAN BE USED MORE THAN ONCE
# =====================================================

def test_compiler_repeated_execution():

    source = """
    a = 10;
    b = a + 5;
    """

    compiler = Compiler(source)

    first_result = compiler.compile()

    second_result = compiler.compile()

    assert isinstance(first_result, list)

    assert isinstance(second_result, list)

    assert len(first_result) > 0

    assert len(second_result) > 0