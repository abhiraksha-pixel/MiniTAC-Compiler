# ============================================================
# MiniTAC Compiler
# Parser
# ============================================================

class ParserError(Exception):

    def __init__(
        self,
        message,
        line=None,
        column=None,
        token=None
    ):
        self.message = message
        self.line = line
        self.column = column
        self.token = token

        super().__init__(message)

    def __str__(self):

        if (
            self.line is not None
            and self.column is not None
        ):
            return (
                f"Parser Error at "
                f"line {self.line}, "
                f"column {self.column}: "
                f"{self.message}"
            )

        return f"Parser Error: {self.message}"


class Parser:

    def __init__(self, tokens):

        self.tokens = tokens
        self.position = 0

    # ========================================================
    # CURRENT TOKEN
    # ========================================================

    def current_token(self):

        if self.position < len(self.tokens):
            return self.tokens[self.position]

        return None

    # ========================================================
    # ADVANCE
    # ========================================================

    def advance(self):

        token = self.current_token()

        if token is not None:
            self.position += 1

        return token

    # ========================================================
    # LAST TOKEN LOCATION
    # ========================================================

    def _last_line(self):

        if self.position > 0:
            token = self.tokens[self.position - 1]
            return getattr(token, "line", None)

        return None

    def _last_column(self):

        if self.position > 0:
            token = self.tokens[self.position - 1]

            column = getattr(
                token,
                "column",
                None
            )

            value = str(
                getattr(
                    token,
                    "value",
                    ""
                )
            )

            if column is not None:
                return column + len(value)

            return column

        return None

    # ========================================================
    # EXPECT
    # ========================================================

    def expect(self, token_type):

        token = self.current_token()

        # ----------------------------------------------------
        # Unexpected end of input
        # ----------------------------------------------------

        if token is None:

            raise ParserError(
                f"Expected {token_type}, "
                f"but reached end of input",
                line=self._last_line(),
                column=self._last_column()
            )

        # ----------------------------------------------------
        # Wrong token
        # ----------------------------------------------------

        if token.token_type != token_type:

            # Special handling for missing semicolon
            if (
                token_type == "SEMICOLON"
                and self.position > 0
            ):

                previous = self.tokens[
                    self.position - 1
                ]

                previous_line = getattr(
                    previous,
                    "line",
                    None
                )

                previous_column = getattr(
                    previous,
                    "column",
                    None
                )

                previous_value = str(
                    getattr(
                        previous,
                        "value",
                        ""
                    )
                )

                if (
                    previous_line is not None
                    and previous_column is not None
                ):

                    error_column = (
                        previous_column
                        + len(previous_value)
                    )

                    raise ParserError(
                        f"Expected SEMICOLON, "
                        f"but found "
                        f"{token.token_type} "
                        f"({token.value})",
                        line=previous_line,
                        column=error_column,
                        token=token
                    )

            # ------------------------------------------------
            # Normal parser error
            # ------------------------------------------------

            raise ParserError(
                f"Expected {token_type}, "
                f"but found "
                f"{token.token_type} "
                f"({token.value})",
                line=getattr(
                    token,
                    "line",
                    None
                ),
                column=getattr(
                    token,
                    "column",
                    None
                ),
                token=token
            )

        self.position += 1

        return token

    # ========================================================
    # PARSE PROGRAM
    # ========================================================

    def parse_program(self):

        statements = []

        while self.current_token() is not None:

            statements.append(
                self.parse_statement()
            )

        return statements

    # ========================================================
    # PARSE STATEMENT
    # ========================================================

    def parse_statement(self):

        token = self.current_token()

        if token is None:

            raise ParserError(
                "Unexpected end of input",
                line=self._last_line(),
                column=self._last_column()
            )

        # ----------------------------------------------------
        # IF
        # ----------------------------------------------------

        if token.token_type == "IF":

            return self.parse_if()

        # ----------------------------------------------------
        # WHILE
        # ----------------------------------------------------

        if token.token_type == "WHILE":

            return self.parse_while()
        # ----------------------------------------------------
        # PRINT
        # ----------------------------------------------------

        if token.token_type == "PRINT":

         return self.parse_print()

        # ----------------------------------------------------
        # BLOCK
        # ----------------------------------------------------

        if token.token_type == "LBRACE":

            return self.parse_block()

        # ----------------------------------------------------
        # ASSIGNMENT
        # ----------------------------------------------------

        if token.token_type == "IDENTIFIER":

            return self.parse_assignment()

        raise ParserError(
            f"Unexpected token: "
            f"{token.token_type} "
            f"({token.value})",
            line=getattr(
                token,
                "line",
                None
            ),
            column=getattr(
                token,
                "column",
                None
            ),
            token=token
        )

    # ========================================================
    # PARSE ASSIGNMENT
    # ========================================================

    def parse_assignment(self):

        variable = self.expect(
            "IDENTIFIER"
        ).value

        self.expect("ASSIGN")

        expression = self.parse_expression()

        self.expect("SEMICOLON")

        return {
            "type": "ASSIGNMENT",
            "variable": variable,
            "expression": expression
        }
    # ========================================================
    # PARSE PRINT
    # ========================================================

    def parse_print(self):

       self.expect("PRINT")

       self.expect("LPAREN")

       expression = self.parse_expression()

       self.expect("RPAREN")

       self.expect("SEMICOLON")

       return {
           "type": "PRINT",
           "expression": expression
    }

    # ========================================================
    # PARSE IF
    # ========================================================

    def parse_if(self):

        self.expect("IF")

        self.expect("LPAREN")

        condition = self.parse_condition()

        self.expect("RPAREN")

        then_branch = self.parse_block()

        else_branch = None

        if (
            self.current_token() is not None
            and self.current_token().token_type == "ELSE"
        ):

            self.advance()

            else_branch = self.parse_block()

        return {
            "type": "IF",
            "condition": condition,
            "then_branch": then_branch,
            "else_branch": else_branch
        }

    # ========================================================
    # PARSE WHILE
    # ========================================================

    def parse_while(self):

        self.expect("WHILE")

        self.expect("LPAREN")

        condition = self.parse_condition()

        self.expect("RPAREN")

        body = self.parse_block()

        return {
            "type": "WHILE",
            "condition": condition,
            "body": body
        }

    # ========================================================
    # PARSE BLOCK
    # ========================================================

    def parse_block(self):

        self.expect("LBRACE")

        statements = []

        while (
            self.current_token() is not None
            and self.current_token().token_type != "RBRACE"
        ):

            statements.append(
                self.parse_statement()
            )

        self.expect("RBRACE")

        return statements

    # ========================================================
    # PARSE CONDITION
    # ========================================================

    def parse_condition(self):

        left = self.parse_expression()

        token = self.current_token()

        if token is None:

            raise ParserError(
                "Expected comparison operator",
                line=self._last_line(),
                column=self._last_column()
            )

        comparison_operators = {

            "GREATER": ">",

            "LESS": "<",

            "GREATER_EQUAL": ">=",

            "LESS_EQUAL": "<=",

            "EQUAL_EQUAL": "==",

            "NOT_EQUAL": "!="
        }

        if token.token_type not in comparison_operators:

            raise ParserError(
                "Expected comparison operator, "
                f"but found {token.token_type} "
                f"({token.value})",
                line=getattr(
                    token,
                    "line",
                    None
                ),
                column=getattr(
                    token,
                    "column",
                    None
                ),
                token=token
            )

        operator = comparison_operators[
            token.token_type
        ]

        self.advance()

        right = self.parse_expression()

        return {
            "type": "CONDITION",
            "operator": operator,
            "left": left,
            "right": right
        }

    # ========================================================
    # PARSE EXPRESSION
    # ========================================================

    def parse_expression(self):

        left = self.parse_term()

        while (
            self.current_token() is not None
            and self.current_token().token_type
            in ["PLUS", "MINUS"]
        ):

            operator_token = self.advance()

            right = self.parse_term()

            left = {
                "type": "BINARY",
                "operator": operator_token.value,
                "left": left,
                "right": right
            }

        return left

    # ========================================================
    # PARSE TERM
    # ========================================================

    def parse_term(self):

        left = self.parse_factor()

        while (
            self.current_token() is not None
            and self.current_token().token_type
            in ["MULTIPLY", "DIVIDE"]
        ):

            operator_token = self.advance()

            right = self.parse_factor()

            left = {
                "type": "BINARY",
                "operator": operator_token.value,
                "left": left,
                "right": right
            }

        return left

    # ========================================================
    # PARSE FACTOR
    # ========================================================

    def parse_factor(self):

        token = self.current_token()

        if token is None:

            raise ParserError(
                "Unexpected end of expression",
                line=self._last_line(),
                column=self._last_column()
            )

        # ----------------------------------------------------
        # NUMBER
        # ----------------------------------------------------

        if token.token_type == "NUMBER":

            self.advance()

            return {
                "type": "NUMBER",
                "value": int(token.value)
            }

        # ----------------------------------------------------
        # IDENTIFIER
        # ----------------------------------------------------

        if token.token_type == "IDENTIFIER":

            self.advance()

            return {
                "type": "IDENTIFIER",
                "name": token.value
            }

        # ----------------------------------------------------
        # PARENTHESES
        # ----------------------------------------------------

        if token.token_type == "LPAREN":

            self.advance()

            expression = self.parse_expression()

            self.expect("RPAREN")

            return expression

        raise ParserError(
            f"Unexpected token in expression: "
            f"{token.token_type} "
            f"({token.value})",
            line=getattr(
                token,
                "line",
                None
            ),
            column=getattr(
                token,
                "column",
                None
            ),
            token=token
        )