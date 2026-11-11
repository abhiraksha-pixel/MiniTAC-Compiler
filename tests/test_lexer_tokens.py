# MiniTAC Compiler
# Automated Lexer Tests
#
# Run with:
# python -m pytest


from lexer import tokenize


def test_basic_assignment():

    source = "a = 10 + 20;"

    tokens = tokenize(source)

    token_types = [
        token.type
        for token in tokens
    ]

    assert token_types == [
        "IDENTIFIER",
        "ASSIGN",
        "NUMBER",
        "PLUS",
        "NUMBER",
        "SEMICOLON"
    ]


def test_multiple_statements():

    source = """
    x = 25;
    y = x + 10;
    """

    tokens = tokenize(source)

    token_types = [
        token.type
        for token in tokens
    ]

    assert token_types == [
        "IDENTIFIER",
        "ASSIGN",
        "NUMBER",
        "SEMICOLON",
        "IDENTIFIER",
        "ASSIGN",
        "IDENTIFIER",
        "PLUS",
        "NUMBER",
        "SEMICOLON"
    ]


def test_parentheses():

    source = "result = (10 + 5) * 2;"

    tokens = tokenize(source)

    token_types = [
        token.type
        for token in tokens
    ]

    assert token_types == [
        "IDENTIFIER",
        "ASSIGN",
        "LPAREN",
        "NUMBER",
        "PLUS",
        "NUMBER",
        "RPAREN",
        "MULTIPLY",
        "NUMBER",
        "SEMICOLON"
    ]


def test_control_flow_tokens():

    source = """
    if (a > 10) {
        b = a + 1;
    }
    else {
        b = 0;
    }
    """

    tokens = tokenize(source)

    token_types = [
        token.type
        for token in tokens
    ]

    assert "IF" in token_types

    assert "ELSE" in token_types

    assert "GREATER" in token_types

    assert "LBRACE" in token_types

    assert "RBRACE" in token_types


def test_while_tokens():

    source = """
    while (b < 20) {
        b = b + 1;
    }
    """

    tokens = tokenize(source)

    token_types = [
        token.type
        for token in tokens
    ]

    assert "WHILE" in token_types

    assert "LESS" in token_types

    assert "LBRACE" in token_types

    assert "RBRACE" in token_types