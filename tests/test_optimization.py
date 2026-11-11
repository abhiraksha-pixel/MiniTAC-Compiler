# MiniTAC Compiler
# Automated Optimization Tests
#
# Run with:
# python -m pytest tests/test_optimization.py -v


from optimizer import Optimizer


def optimize(tac):

    optimizer = Optimizer(tac)

    optimized = optimizer.optimize()

    return optimized


# =====================================================
# CONSTANT FOLDING
# =====================================================

def test_constant_folding():

    tac = [
        "t1 = 10 + 20",
        "a = t1"
    ]

    result = optimize(tac)

    assert "a = 30" in result


# =====================================================
# CONSTANT PROPAGATION
# =====================================================

def test_constant_propagation():

    tac = [
        "a = 10",
        "b = a"
    ]

    result = optimize(tac)

    assert "a = 10" in result

    assert "b = 10" in result


# =====================================================
# ALGEBRAIC SIMPLIFICATION
# =====================================================

def test_algebraic_simplification():

    tac = [
        "t1 = x + 0",
        "a = t1",
        "t2 = y * 1",
        "b = t2"
    ]

    result = optimize(tac)

    assert "a = x" in result

    assert "b = y" in result


# =====================================================
# COPY PROPAGATION
# =====================================================

def test_copy_propagation():

    tac = [
        "a = x",
        "b = a",
        "c = b"
    ]

    result = optimize(tac)

    assert "b = x" in result

    assert "c = x" in result


# =====================================================
# COMMON SUBEXPRESSION ELIMINATION
# =====================================================

def test_common_subexpression_elimination():

    tac = [
        "t1 = x + y",
        "a = t1",
        "t2 = x + y",
        "b = t2"
    ]

    result = optimize(tac)

    # First expression remains.

    assert "t1 = x + y" in result

    # Second expression should reuse t1.

    assert "b = t1" in result


# =====================================================
# DEAD CODE ELIMINATION
# =====================================================

def test_dead_code_elimination():

    tac = [
        "t1 = 10",
        "t2 = 20",
        "a = 5"
    ]

    result = optimize(tac)

    assert "a = 5" in result

    assert "t1 = 10" not in result

    assert "t2 = 20" not in result


# =====================================================
# MULTIPLE OPTIMIZATIONS
# =====================================================

def test_multiple_optimizations():

    tac = [
        "a = 10",
        "t1 = a + 0",
        "b = t1",
        "t2 = 20 + 30",
        "c = t2"
    ]

    result = optimize(tac)

    assert "a = 10" in result

    assert "b = 10" in result

    assert "c = 50" in result


# =====================================================
# CONTROL FLOW SAFETY
# =====================================================

def test_loop_is_not_broken():

    tac = [
        "L1:",
        "if d < 20 goto L2",
        "goto L3",
        "L2:",
        "t1 = d + 1",
        "d = t1",
        "goto L1",
        "L3:"
    ]

    result = optimize(tac)

    # The loop increment must remain.

    assert any(
        "d + 1" in instruction
        for instruction in result
    )

    # The optimizer must NOT incorrectly turn
    # the loop increment into d = 1.

    assert "d = 1" not in result


# =====================================================
# STATISTICS
# =====================================================

def test_optimization_statistics():

    tac = [
        "t1 = 10 + 20",
        "a = t1"
    ]

    optimizer = Optimizer(tac)

    result = optimizer.optimize()

    stats = optimizer.get_statistics()

    assert "a = 30" in result

    assert (
        stats["constant_folding"] > 0
    )