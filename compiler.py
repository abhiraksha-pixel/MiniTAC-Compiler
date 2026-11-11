# MiniTAC Compiler
# Main Compiler Pipeline
#
# Pipeline:
#
# Source
#   ↓
# Lexer
#   ↓
# Parser
#   ↓
# AST
#   ↓
# TAC
#   ↓
# Optimizer
#   ↓
# CFG
#   ↓
# Liveness Analysis
#   ↓
# Dead Code Elimination
#   ↓
# Final TAC


from lexer import tokenize
from parser import Parser
from tac import TACGenerator
from optimizer import Optimizer
from cfg import ControlFlowGraph
from dataflow import LivenessAnalyzer
from dce import DeadCodeEliminator


class Compiler:

    def __init__(self, source):

        self.source = source

        self.tokens = []

        self.ast = []

        self.tac = []

        self.optimized_tac = []

        self.cfg = None

        self.liveness = None

        self.dce = None

        self.optimizer_statistics = {}

        self.dce_removed = 0

        self.program_output = []

    # =====================================================
    # COMPILE
    # =====================================================

    def compile(self):

        # ---------------------------------------------
        # STEP 1 — LEXICAL ANALYSIS
        # ---------------------------------------------

        self.tokens = tokenize(
            self.source
        )

        # ---------------------------------------------
        # STEP 2 — PARSING
        # ---------------------------------------------

        parser = Parser(
            self.tokens
        )

        self.ast = parser.parse_program()

        # ---------------------------------------------
        # STEP 3 — TAC GENERATION
        # ---------------------------------------------

        generator = TACGenerator()

        self.tac = generator.generate(
            self.ast
        )

        # ---------------------------------------------
        # STEP 4 — TRADITIONAL OPTIMIZATION
        # ---------------------------------------------

        optimizer = Optimizer(
            self.tac
        )

        optimized = optimizer.optimize()

        self.optimizer_statistics = (
            optimizer.get_statistics()
        )

        # ---------------------------------------------
        # STEP 5 — BUILD CFG
        # ---------------------------------------------

        self.cfg = ControlFlowGraph(
            optimized
        )

        self.cfg.build()

        # ---------------------------------------------
        # STEP 6 — LIVENESS ANALYSIS
        # ---------------------------------------------

        self.liveness = LivenessAnalyzer(
            self.cfg
        )

        self.liveness.analyze()

        # ---------------------------------------------
        # STEP 7 — DEAD CODE ELIMINATION
        # ---------------------------------------------

        self.dce = DeadCodeEliminator(
            self.cfg,
            self.liveness
        )

        optimized_blocks = (
            self.dce.eliminate()
        )

        self.optimized_tac = (
            self.dce.get_optimized_tac(
                optimized_blocks
            )
        )

        self.dce_removed = (
            self.dce.get_removed_count()
        )

        # ---------------------------------------------
        # STEP 8 — PROGRAM EXECUTION
        # ---------------------------------------------

        self.execute()

        return self.optimized_tac

        # =====================================================
    # EXECUTE FINAL TAC
    # =====================================================

    def execute(self):

        variables = {}
        output = []

        # -------------------------------------------------
        # STEP 1 — BUILD LABEL TABLE
        # -------------------------------------------------

        labels = {}

        for index, instruction in enumerate(
            self.optimized_tac
        ):

            parts = instruction.split()

            if (
                len(parts) == 1
                and parts[0].endswith(":")
            ):

                label = parts[0][:-1]

                labels[label] = index

        # -------------------------------------------------
        # STEP 2 — EXECUTE TAC USING PROGRAM COUNTER
        # -------------------------------------------------

        pc = 0

        # Safety limit prevents accidental infinite loops.
        steps = 0
        max_steps = 100000

        while pc < len(self.optimized_tac):

            steps += 1

            if steps > max_steps:

                raise Exception(
                    "Program execution stopped: "
                    "possible infinite loop."
                )

            instruction = self.optimized_tac[pc]

            parts = instruction.split()

            # -------------------------------------------------
            # LABEL
            # -------------------------------------------------

            if (
                len(parts) == 1
                and parts[0].endswith(":")
            ):

                pc += 1
                continue

            # -------------------------------------------------
            # PRINT
            # -------------------------------------------------

            if (
                len(parts) == 2
                and parts[0] == "PRINT"
            ):

                value = parts[1]

                if value in variables:

                    value = variables[value]

                output.append(
                    str(value)
                )

                pc += 1
                continue

            # -------------------------------------------------
            # UNCONDITIONAL GOTO
            #
            # Example:
            #
            # goto L1
            # -------------------------------------------------

            if (
                len(parts) == 2
                and parts[0] == "goto"
            ):

                label = parts[1]

                if label not in labels:

                    raise Exception(
                        f"Unknown label: {label}"
                    )

                pc = labels[label]

                continue

            # -------------------------------------------------
            # CONDITIONAL GOTO
            #
            # Example:
            #
            # if i <= 5 goto L1
            # -------------------------------------------------

            if (
                len(parts) == 6
                and parts[0] == "if"
                and parts[4] == "goto"
            ):

                left = parts[1]
                operator = parts[2]
                right = parts[3]
                label = parts[5]

                # Resolve variables

                if left in variables:

                    left = variables[left]

                else:

                    left = int(left)

                if right in variables:

                    right = variables[right]

                else:

                    right = int(right)

                # Evaluate condition

                condition = False

                if operator == "==":

                    condition = (
                        left == right
                    )

                elif operator == "!=":

                    condition = (
                        left != right
                    )

                elif operator == "<":

                    condition = (
                        left < right
                    )

                elif operator == "<=":

                    condition = (
                        left <= right
                    )

                elif operator == ">":

                    condition = (
                        left > right
                    )

                elif operator == ">=":

                    condition = (
                        left >= right
                    )

                else:

                    raise Exception(
                        f"Unknown comparison operator: "
                        f"{operator}"
                    )

                # Jump if condition is true

                if condition:

                    if label not in labels:

                        raise Exception(
                            f"Unknown label: {label}"
                        )

                    pc = labels[label]

                else:

                    pc += 1

                continue

            # -------------------------------------------------
            # SIMPLE ASSIGNMENT
            #
            # Example:
            #
            # i = 1
            # -------------------------------------------------

            if len(parts) == 3:

                target = parts[0]
                value = parts[2]

                if value in variables:

                    value = variables[value]

                else:

                    value = int(value)

                variables[target] = value

                pc += 1
                continue

            # -------------------------------------------------
            # BINARY EXPRESSION
            #
            # Example:
            #
            # t1 = i + sum
            # -------------------------------------------------

            if len(parts) == 5:

                target = parts[0]

                left = parts[2]
                operator = parts[3]
                right = parts[4]

                # Resolve left operand

                if left in variables:

                    left = variables[left]

                else:

                    left = int(left)

                # Resolve right operand

                if right in variables:

                    right = variables[right]

                else:

                    right = int(right)

                # Perform operation

                if operator == "+":

                    result = (
                        left + right
                    )

                elif operator == "-":

                    result = (
                        left - right
                    )

                elif operator == "*":

                    result = (
                        left * right
                    )

                elif operator == "/":

                    if right == 0:

                        raise Exception(
                            "Division by zero."
                        )

                    result = (
                        left // right
                    )

                else:

                    raise Exception(
                        f"Unknown operator: "
                        f"{operator}"
                    )

                variables[target] = result

                pc += 1
                continue

            # -------------------------------------------------
            # UNKNOWN INSTRUCTION
            # -------------------------------------------------

            raise Exception(
                f"Unknown TAC instruction: "
                f"{instruction}"
            )

        # -------------------------------------------------
        # SAVE PROGRAM OUTPUT
        # -------------------------------------------------

        self.program_output = output

        return output


    

    # =====================================================
    # GET RESULTS
    # =====================================================

    def get_results(self):

        return {

            "source": self.source,

            "tokens": self.tokens,

            "ast": self.ast,

            "tac": self.tac,

            "optimized_tac": self.optimized_tac,

            "cfg": self.cfg,

            "liveness": self.liveness,

            "optimizer_statistics":
                self.optimizer_statistics,

            "dce_removed":
                self.dce_removed,

            "program_output":
                self.program_output
        }