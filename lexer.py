# MiniTAC Compiler
# Lexical Analyzer
#
# Converts source code into tokens.


# =====================================================
# TOKEN CLASS
# =====================================================

class Token:

    def __init__(self, token_type, value, line=None, column=None):

        # Keep token_type because the parser uses it.
        self.token_type = token_type

        # Also keep type for convenience.
        self.type = token_type

        self.value = value

        # Source location
        self.line = line
        self.column = column

    def __repr__(self):

        return (
            f"Token({self.token_type}, "
            f"{self.value}, "
            f"line={self.line}, "
            f"column={self.column})"
        )


# =====================================================
# KEYWORDS
# =====================================================

KEYWORDS = {
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "print": "PRINT"
}

# =====================================================
# TOKENIZE
# =====================================================

def tokenize(source):

    tokens = []

    i = 0

    # Track source position
    line = 1
    column = 1

    while i < len(source):

        char = source[i]

        # =================================================
        # WHITESPACE
        # =================================================

        if char.isspace():

            if char == "\n":
                line += 1
                column = 1
            else:
                column += 1

            i += 1

            continue

        # =================================================
        # IDENTIFIERS / KEYWORDS
        # =================================================

        if char.isalpha() or char == "_":

            start = i
            start_column = column

            while (
                i < len(source)
                and (
                    source[i].isalnum()
                    or source[i] == "_"
                )
            ):
                i += 1
                column += 1

            word = source[start:i]

            if word in KEYWORDS:

                tokens.append(
                    Token(
                        KEYWORDS[word],
                        word,
                        line,
                        start_column
                    )
                )

            else:

                tokens.append(
                    Token(
                        "IDENTIFIER",
                        word,
                        line,
                        start_column
                    )
                )

            continue

        # =================================================
        # NUMBERS
        # =================================================

        if char.isdigit():

            start = i
            start_column = column

            while (
                i < len(source)
                and source[i].isdigit()
            ):
                i += 1
                column += 1

            number = source[start:i]

            tokens.append(
                Token(
                    "NUMBER",
                    number,
                    line,
                    start_column
                )
            )

            continue

        # =================================================
        # TWO-CHARACTER OPERATORS
        # =================================================

        if i + 1 < len(source):

            two_char = source[i:i + 2]

            if two_char == ">=":

                tokens.append(
                    Token(
                        "GREATER_EQUAL",
                        ">=",
                        line,
                        column
                    )
                )

                i += 2
                column += 2

                continue

            if two_char == "<=":

                tokens.append(
                    Token(
                        "LESS_EQUAL",
                        "<=",
                        line,
                        column
                    )
                )

                i += 2
                column += 2

                continue

            if two_char == "==":

                tokens.append(
                    Token(
                        "EQUAL_EQUAL",
                        "==",
                        line,
                        column
                    )
                )

                i += 2
                column += 2

                continue

            if two_char == "!=":

                tokens.append(
                    Token(
                        "NOT_EQUAL",
                        "!=",
                        line,
                        column
                    )
                )

                i += 2
                column += 2

                continue

        # =================================================
        # SINGLE-CHARACTER TOKENS
        # =================================================

        single_char_tokens = {

            "=": "ASSIGN",

            "+": "PLUS",

            "-": "MINUS",

            "*": "MULTIPLY",

            "/": "DIVIDE",

            ">": "GREATER",

            "<": "LESS",

            "(": "LPAREN",

            ")": "RPAREN",

            "{": "LBRACE",

            "}": "RBRACE",

            ";": "SEMICOLON"
        }

        if char in single_char_tokens:

            tokens.append(
                Token(
                    single_char_tokens[char],
                    char,
                    line,
                    column
                )
            )

            i += 1
            column += 1

            continue

        # =================================================
        # UNKNOWN CHARACTER
        # =================================================

        raise Exception(
            f"Lexer Error: Unknown character "
            f"'{char}' at line {line}, column {column}"
        )

    return tokens