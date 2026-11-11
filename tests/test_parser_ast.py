# MiniTAC Compiler
# Automated Parser Tests
#
# Run with:
# python -m pytest tests/test_parser.py -v


from lexer import tokenize
from parser import Parser


def parse_source(source):

    tokens = tokenize(source)

    parser = Parser(tokens)

    return parser.parse_program()


# =====================================================
# SIMPLE ASSIGNMENT
# =====================================================

def test_simple_assignment():

    ast = parse_source(
        "a = 10;"
    )

    assert len(ast) == 1

    statement = ast[0]

    assert statement["type"] == "ASSIGNMENT"

    assert statement["variable"] == "a"

    assert statement["expression"]["type"] == "NUMBER"

    assert statement["expression"]["value"] == 10


# =====================================================
# OPERATOR PRECEDENCE
# =====================================================

def test_operator_precedence():

    ast = parse_source(
        "a = 10 + 20 * 3;"
    )

    expression = ast[0]["expression"]

    # The top-level operation should be +
    assert expression["type"] == "BINARY"

    assert expression["operator"] == "+"

    # Left side should be 10
    assert expression["left"]["value"] == 10

    # Right side should be 20 * 3
    right = expression["right"]

    assert right["type"] == "BINARY"

    assert right["operator"] == "*"

    assert right["left"]["value"] == 20

    assert right["right"]["value"] == 3


# =====================================================
# PARENTHESES
# =====================================================

def test_parentheses():

    ast = parse_source(
        "result = (10 + 5) * 2;"
    )

    expression = ast[0]["expression"]

    assert expression["type"] == "BINARY"

    assert expression["operator"] == "*"

    left = expression["left"]

    assert left["type"] == "BINARY"

    assert left["operator"] == "+"

    assert left["left"]["value"] == 10

    assert left["right"]["value"] == 5

    assert expression["right"]["value"] == 2


# =====================================================
# MULTIPLE STATEMENTS
# =====================================================

def test_multiple_statements():

    ast = parse_source(
        """
        x = 25;
        y = x + 10;
        """
    )

    assert len(ast) == 2

    assert ast[0]["variable"] == "x"

    assert ast[1]["variable"] == "y"

    expression = ast[1]["expression"]

    assert expression["operator"] == "+"

    assert expression["left"]["name"] == "x"

    assert expression["right"]["value"] == 10


# =====================================================
# IF / ELSE
# =====================================================

def test_if_else():

    ast = parse_source(
        """
        if (a > 10) {
            b = a + 1;
        }
        else {
            b = 0;
        }
        """
    )

    assert len(ast) == 1

    statement = ast[0]

    assert statement["type"] == "IF"

    # Condition

    condition = statement["condition"]

    assert condition["type"] == "CONDITION"

    assert condition["operator"] == ">"

    assert condition["left"]["name"] == "a"

    assert condition["right"]["value"] == 10

    # Then branch

    then_branch = statement["then_branch"]

    assert len(then_branch) == 1

    assert then_branch[0]["type"] == "ASSIGNMENT"

    assert then_branch[0]["variable"] == "b"

    # Else branch

    else_branch = statement["else_branch"]

    assert len(else_branch) == 1

    assert else_branch[0]["type"] == "ASSIGNMENT"

    assert else_branch[0]["variable"] == "b"

    assert (
        else_branch[0]["expression"]["value"]
        == 0
    )


# =====================================================
# WHILE
# =====================================================

def test_while():

    ast = parse_source(
        """
        while (b < 20) {
            b = b + 1;
        }
        """
    )

    assert len(ast) == 1

    statement = ast[0]

    assert statement["type"] == "WHILE"

    condition = statement["condition"]

    assert condition["type"] == "CONDITION"

    assert condition["operator"] == "<"

    assert condition["left"]["name"] == "b"

    assert condition["right"]["value"] == 20

    body = statement["body"]

    assert len(body) == 1

    assignment = body[0]

    assert assignment["type"] == "ASSIGNMENT"

    assert assignment["variable"] == "b"

    expression = assignment["expression"]

    assert expression["type"] == "BINARY"

    assert expression["operator"] == "+"

    assert expression["left"]["name"] == "b"

    assert expression["right"]["value"] == 1