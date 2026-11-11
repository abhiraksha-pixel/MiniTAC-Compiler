# MiniTAC Compiler
# Three-Address Code Generator
#
# Supported:
# - Assignments
# - Arithmetic expressions
# - if
# - else
# - while
# - Conditions
# - Labels
# - Conditional jumps
# - Unconditional jumps


class TACGenerator:

    def __init__(self):

        # Temporary variable counter
        self.temp_count = 0

        # Label counter
        self.label_count = 0

        # Generated TAC instructions
        self.instructions = []

    # =====================================================
    # CREATE TEMPORARY VARIABLE
    # =====================================================

    def new_temp(self):

        self.temp_count += 1

        return f"t{self.temp_count}"

    # =====================================================
    # CREATE LABEL
    # =====================================================

    def new_label(self):

        self.label_count += 1

        return f"L{self.label_count}"

    # =====================================================
    # ADD INSTRUCTION
    # =====================================================

    def emit(self, instruction):

        self.instructions.append(instruction)

    # =====================================================
    # GENERATE TAC
    # =====================================================

    def generate(self, ast):

        # Reset previous state

        self.instructions = []

        self.temp_count = 0

        self.label_count = 0

        # Generate code for each statement

        for statement in ast:

            self.generate_statement(statement)

        return self.instructions

    # =====================================================
    # GENERATE STATEMENT
    # =====================================================

    def generate_statement(self, statement):

        statement_type = statement["type"]

        # ---------------------------------------------
        # ASSIGNMENT
        # ---------------------------------------------

        if statement_type == "ASSIGNMENT":

            variable = statement["variable"]

            expression = statement["expression"]

            value = self.generate_expression(
                expression
            )

            self.emit(
                f"{variable} = {value}"
            )

        # ---------------------------------------------
        # IF
        # ---------------------------------------------

        elif statement_type == "IF":

            self.generate_if(statement)

        # ---------------------------------------------
        # WHILE
        # ---------------------------------------------

        elif statement_type == "WHILE":

            self.generate_while(statement)

    # ---------------------------------------------
    # PRINT
    # ---------------------------------------------

        elif statement_type == "PRINT":

            expression = statement["expression"]

            value = self.generate_expression(
                expression
           )

            self.emit(
               f"PRINT {value}"
    )

        else:

            raise Exception(
                f"Unknown statement type: "
                f"{statement_type}"
            )

    # =====================================================
    # GENERATE IF / ELSE
    # =====================================================

    def generate_if(self, statement):

        condition = statement["condition"]

        then_branch = statement["then_branch"]

        else_branch = statement["else_branch"]

        # Create labels

        then_label = self.new_label()

        end_label = self.new_label()

        # If there is an else branch,
        # create an else label.

        if else_branch is not None:

            else_label = self.new_label()

        else:

            else_label = end_label

        # ---------------------------------------------
        # Generate condition
        # ---------------------------------------------

        left = self.generate_expression(
            condition["left"]
        )

        right = self.generate_expression(
            condition["right"]
        )

        operator = condition["operator"]

        # ---------------------------------------------
        # Conditional jump
        # ---------------------------------------------

        self.emit(
            f"if {left} {operator} "
            f"{right} goto {then_label}"
        )

        # ---------------------------------------------
        # False branch
        # ---------------------------------------------

        self.emit(
            f"goto {else_label}"
        )

        # ---------------------------------------------
        # THEN LABEL
        # ---------------------------------------------

        self.emit(
            f"{then_label}:"
        )

        # Generate THEN statements

        for statement_item in then_branch:

            self.generate_statement(
                statement_item
            )

        # Jump to end after THEN branch

        self.emit(
            f"goto {end_label}"
        )

        # ---------------------------------------------
        # ELSE LABEL
        # ---------------------------------------------

        if else_branch is not None:

            self.emit(
                f"{else_label}:"
            )

            # Generate ELSE statements

            for statement_item in else_branch:

                self.generate_statement(
                    statement_item
                )

        # ---------------------------------------------
        # END LABEL
        # ---------------------------------------------

        self.emit(
            f"{end_label}:"
        )

    # =====================================================
    # GENERATE WHILE
    # =====================================================

    def generate_while(self, statement):

        condition = statement["condition"]

        body = statement["body"]

        # Create labels

        condition_label = self.new_label()

        body_label = self.new_label()

        end_label = self.new_label()

        # ---------------------------------------------
        # CONDITION LABEL
        # ---------------------------------------------

        self.emit(
            f"{condition_label}:"
        )

        # ---------------------------------------------
        # Generate condition operands
        # ---------------------------------------------

        left = self.generate_expression(
            condition["left"]
        )

        right = self.generate_expression(
            condition["right"]
        )

        operator = condition["operator"]

        # ---------------------------------------------
        # Conditional jump
        # ---------------------------------------------

        self.emit(
            f"if {left} {operator} "
            f"{right} goto {body_label}"
        )

        # ---------------------------------------------
        # Exit loop
        # ---------------------------------------------

        self.emit(
            f"goto {end_label}"
        )

        # ---------------------------------------------
        # LOOP BODY
        # ---------------------------------------------

        self.emit(
            f"{body_label}:"
        )

        for statement_item in body:

            self.generate_statement(
                statement_item
            )

        # ---------------------------------------------
        # Go back to condition
        # ---------------------------------------------

        self.emit(
            f"goto {condition_label}"
        )

        # ---------------------------------------------
        # END LOOP
        # ---------------------------------------------

        self.emit(
            f"{end_label}:"
        )

    # =====================================================
    # GENERATE EXPRESSION
    # =====================================================

    def generate_expression(self, expression):

        expression_type = expression["type"]

        # ---------------------------------------------
        # NUMBER
        # ---------------------------------------------

        if expression_type == "NUMBER":

            return str(
                expression["value"]
            )

        # ---------------------------------------------
        # IDENTIFIER
        # ---------------------------------------------

        if expression_type == "IDENTIFIER":

            return expression["name"]

        # ---------------------------------------------
        # BINARY EXPRESSION
        # ---------------------------------------------

        if expression_type == "BINARY":

            left = self.generate_expression(
                expression["left"]
            )

            right = self.generate_expression(
                expression["right"]
            )

            operator = expression["operator"]

            temp = self.new_temp()

            self.emit(
                f"{temp} = "
                f"{left} {operator} {right}"
            )

            return temp

        raise Exception(
            f"Unknown expression type: "
            f"{expression_type}"
        )