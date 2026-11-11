# MiniTAC Compiler
# Automated Three-Address Code Tests
#
# Run with:
# python -m pytest tests/test_tac_generation.py -v


from lexer import tokenize
from parser import Parser
from tac import TACGenerator


def generate_tac(source):
    """
    Convert source code into TAC.
    """

    tokens = tokenize(source)

    parser = Parser(tokens)

    ast = parser.parse_program()

    generator = TACGenerator()

    return generator.generate(ast)


# =====================================================
# SIMPLE ASSIGNMENT
# =====================================================

def test_simple_assignment():

    tac = generate_tac(
        "a = 10;"
    )

    assert tac == [
        "a = 10"
    ]


# =====================================================
# ARITHMETIC EXPRESSION
# =====================================================

def test_arithmetic_expression():

    tac = generate_tac(
        "a = 10 + 20 * 3;"
    )

    assert tac == [
        "t1 = 20 * 3",
        "t2 = 10 + t1",
        "a = t2"
    ]


# =====================================================
# OPERATOR PRECEDENCE
# =====================================================

def test_operator_precedence():

    tac = generate_tac(
        "result = (10 + 5) * 2;"
    )

    assert tac == [
        "t1 = 10 + 5",
        "t2 = t1 * 2",
        "result = t2"
    ]


# =====================================================
# MULTIPLE STATEMENTS
# =====================================================

def test_multiple_statements():

    tac = generate_tac(
        """
        a = 10;
        b = a + 5;
        """
    )

    assert tac == [
        "a = 10",
        "t1 = a + 5",
        "b = t1"
    ]


# =====================================================
# IF / ELSE
# =====================================================

def test_if_else():

    tac = generate_tac(
        """
        a = 15;

        if (a > 10) {
            b = a + 1;
        }
        else {
            b = 0;
        }
        """
    )

    # Basic instructions must exist.

    assert "a = 15" in tac

    # Conditional jump must exist.

    assert any(
        instruction.startswith(
            "if a > 10 goto"
        )
        for instruction in tac
    )

    # Else branch assignment.

    assert "b = 0" in tac

    # Then branch must contain a + 1.

    assert any(
        "a + 1" in instruction
        for instruction in tac
    )

    # Labels must be generated.

    assert any(
        instruction.startswith("L")
        and instruction.endswith(":")
        for instruction in tac
    )


# =====================================================
# WHILE LOOP
# =====================================================

def test_while_loop():

    tac = generate_tac(
        """
        b = 10;

        while (b < 20) {
            b = b + 1;
        }
        """
    )

    # Initial assignment.

    assert "b = 10" in tac

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

    # Backward goto should exist.

    labels = [
        instruction[:-1]
        for instruction in tac
        if (
            instruction.startswith("L")
            and instruction.endswith(":")
        )
    ]

    assert len(labels) >= 2

    # At least one goto must target a label.

    assert any(
        instruction.startswith("goto L")
        for instruction in tac
    )


# =====================================================
# CONTROL FLOW COMBINATION
# =====================================================

def test_if_and_while_together():

    tac = generate_tac(
        """
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
    )

    # Assignment

    assert "a = 15" in tac

    # IF

    assert any(
        instruction.startswith(
            "if a > 10 goto"
        )
        for instruction in tac
    )

    # ELSE

    assert "b = 0" in tac

    # WHILE

    assert any(
        instruction.startswith(
            "if b < 20 goto"
        )
        for instruction in tac
    )

    # Loop body

    assert any(
        "b + 1" in instruction
        for instruction in tac
    )

    # There should be several labels.

    labels = [
        instruction
        for instruction in tac
        if (
            instruction.startswith("L")
            and instruction.endswith(":")
        )
    ]

    assert len(labels) >= 4