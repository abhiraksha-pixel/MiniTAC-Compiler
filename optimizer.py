# MiniTAC Compiler
# Control-Flow-Aware TAC Optimizer
#
# Optimizations:
# 1. Constant Folding
# 2. Constant Propagation
# 3. Algebraic Simplification
# 4. Copy Propagation
# 5. Common Subexpression Elimination
# 6. Dead Code Elimination
#
# Design:
# - Straight-line programs are optimized aggressively.
# - Programs containing control flow are optimized block-by-block.
# - No constant/copy information crosses labels or jumps.


class Optimizer:

    def __init__(self, instructions):

        self.instructions = instructions

        self.stats = {
            "constant_folding": 0,
            "constant_propagation": 0,
            "algebraic_simplification": 0,
            "copy_propagation": 0,
            "common_subexpression_elimination": 0,
            "dead_code_elimination": 0
        }

    # =====================================================
    # BASIC HELPERS
    # =====================================================

    def is_number(self, value):

        return value.lstrip("-").isdigit()

    def is_temporary(self, value):

        return (
            value.startswith("t")
            and value[1:].isdigit()
        )

    def is_label(self, instruction):

        parts = instruction.split()

        return (
            len(parts) == 1
            and parts[0].endswith(":")
        )

    def is_conditional_jump(self, instruction):

        parts = instruction.split()

        return (
            len(parts) == 6
            and parts[0] == "if"
            and parts[4] == "goto"
        )

    def is_unconditional_jump(self, instruction):

        parts = instruction.split()

        return (
            len(parts) == 2
            and parts[0] == "goto"
        )

    def contains_control_flow(self):

        for instruction in self.instructions:

            if (
                self.is_label(instruction)
                or
                self.is_conditional_jump(
                    instruction
                )
                or
                self.is_unconditional_jump(
                    instruction
                )
            ):

                return True

        return False

    # =====================================================
    # ARITHMETIC
    # =====================================================

    def calculate(self, left, operator, right):

        left = int(left)
        right = int(right)

        if operator == "+":

            return left + right

        if operator == "-":

            return left - right

        if operator == "*":

            return left * right

        if operator == "/":

            if right == 0:

                return None

            return left // right

        return None

    # =====================================================
    # CONSTANT FOLDING
    # =====================================================

    def constant_folding(self, instructions):

        result = []

        for instruction in instructions:

            parts = instruction.split()

            if len(parts) == 5:

                target = parts[0]

                left = parts[2]

                operator = parts[3]

                right = parts[4]

                if (
                    self.is_number(left)
                    and self.is_number(right)
                ):

                    value = self.calculate(
                        left,
                        operator,
                        right
                    )

                    if value is not None:

                        result.append(
                            f"{target} = {value}"
                        )

                        self.stats[
                            "constant_folding"
                        ] += 1

                        continue

            result.append(instruction)

        return result

    # =====================================================
    # CONSTANT PROPAGATION
    # =====================================================

    def constant_propagation(
        self,
        instructions
    ):

        constants = {}

        result = []

        for instruction in instructions:

            parts = instruction.split()

            # -----------------------------------------
            # Simple assignment
            # -----------------------------------------

            if len(parts) == 3:

                target = parts[0]

                value = parts[2]

                if value in constants:

                    value = constants[value]

                    self.stats[
                        "constant_propagation"
                    ] += 1

                if self.is_number(value):

                    constants[target] = value

                else:

                    constants.pop(
                        target,
                        None
                    )

                result.append(
                    f"{target} = {value}"
                )

                continue

            # -----------------------------------------
            # Binary expression
            # -----------------------------------------

            if len(parts) == 5:

                target = parts[0]

                left = parts[2]

                operator = parts[3]

                right = parts[4]

                if left in constants:

                    left = constants[left]

                    self.stats[
                        "constant_propagation"
                    ] += 1

                if right in constants:

                    right = constants[right]

                    self.stats[
                        "constant_propagation"
                    ] += 1

                if (
                    self.is_number(left)
                    and self.is_number(right)
                ):

                    value = self.calculate(
                        left,
                        operator,
                        right
                    )

                    if value is not None:

                        result.append(
                            f"{target} = {value}"
                        )

                        constants[target] = str(
                            value
                        )

                        self.stats[
                            "constant_folding"
                        ] += 1

                        continue

                result.append(
                    f"{target} = "
                    f"{left} {operator} {right}"
                )

                constants.pop(
                    target,
                    None
                )

                continue

            result.append(instruction)

        return result

    # =====================================================
    # ALGEBRAIC SIMPLIFICATION
    # =====================================================

    def algebraic_simplification(
        self,
        instructions
    ):

        result = []

        for instruction in instructions:

            parts = instruction.split()

            if len(parts) == 5:

                target = parts[0]

                left = parts[2]

                operator = parts[3]

                right = parts[4]

                # x + 0

                if (
                    operator == "+"
                    and right == "0"
                ):

                    result.append(
                        f"{target} = {left}"
                    )

                    self.stats[
                        "algebraic_simplification"
                    ] += 1

                    continue

                # x - 0

                if (
                    operator == "-"
                    and right == "0"
                ):

                    result.append(
                        f"{target} = {left}"
                    )

                    self.stats[
                        "algebraic_simplification"
                    ] += 1

                    continue

                # x * 1

                if (
                    operator == "*"
                    and right == "1"
                ):

                    result.append(
                        f"{target} = {left}"
                    )

                    self.stats[
                        "algebraic_simplification"
                    ] += 1

                    continue

                # x / 1

                if (
                    operator == "/"
                    and right == "1"
                ):

                    result.append(
                        f"{target} = {left}"
                    )

                    self.stats[
                        "algebraic_simplification"
                    ] += 1

                    continue

                # x * 0

                if (
                    operator == "*"
                    and right == "0"
                ):

                    result.append(
                        f"{target} = 0"
                    )

                    self.stats[
                        "algebraic_simplification"
                    ] += 1

                    continue

                # 0 * x

                if (
                    operator == "*"
                    and left == "0"
                ):

                    result.append(
                        f"{target} = 0"
                    )

                    self.stats[
                        "algebraic_simplification"
                    ] += 1

                    continue

            result.append(instruction)

        return result

    # =====================================================
    # COPY PROPAGATION
    # =====================================================

    def copy_propagation(
        self,
        instructions
    ):

        copies = {}

        result = []

        for instruction in instructions:

            parts = instruction.split()

            # -----------------------------------------
            # Simple assignment
            # -----------------------------------------

            if len(parts) == 3:

                target = parts[0]

                value = parts[2]

                # Follow copy chain.

                visited = set()

                while (
                    value in copies
                    and value not in visited
                ):

                    visited.add(value)

                    value = copies[value]

                if (
                    value != target
                    and not self.is_number(value)
                ):

                    copies[target] = value

                else:

                    copies.pop(
                        target,
                        None
                    )

                result.append(
                    f"{target} = {value}"
                )

                continue

            # -----------------------------------------
            # Binary expression
            # -----------------------------------------

            if len(parts) == 5:

                target = parts[0]

                left = parts[2]

                operator = parts[3]

                right = parts[4]

                visited = set()

                while (
                    left in copies
                    and left not in visited
                ):

                    visited.add(left)

                    left = copies[left]

                    self.stats[
                        "copy_propagation"
                    ] += 1

                visited = set()

                while (
                    right in copies
                    and right not in visited
                ):

                    visited.add(right)

                    right = copies[right]

                    self.stats[
                        "copy_propagation"
                    ] += 1

                result.append(
                    f"{target} = "
                    f"{left} {operator} {right}"
                )

                copies.pop(
                    target,
                    None
                )

                continue

            result.append(instruction)

        return result

    # =====================================================
    # COMMON SUBEXPRESSION ELIMINATION
    # =====================================================

    def common_subexpression_elimination(
        self,
        instructions
    ):

        expressions = {}

        result = []

        for instruction in instructions:

            parts = instruction.split()

            if len(parts) == 5:

                target = parts[0]

                left = parts[2]

                operator = parts[3]

                right = parts[4]

                expression = (
                    left,
                    operator,
                    right
                )

                if expression in expressions:

                    previous = expressions[
                        expression
                    ]

                    result.append(
                        f"{target} = {previous}"
                    )

                    self.stats[
                        "common_subexpression_elimination"
                    ] += 1

                else:

                    result.append(
                        instruction
                    )

                expressions[
                    expression
                ] = target

                continue

            # If a variable is overwritten, expressions
            # involving that variable can no longer
            # safely be reused.

            if len(parts) == 3:

                target = parts[0]

                expressions = {
                    key: value
                    for key, value in expressions.items()
                    if target not in key
                }

            result.append(instruction)

        return result

    # =====================================================
    # DEAD CODE ELIMINATION
    # =====================================================

    def dead_code_elimination(
        self,
        instructions
    ):

        used = set()

        # ---------------------------------------------
        # Collect used values.
        # ---------------------------------------------

        for instruction in instructions:

            parts = instruction.split()

            # Binary expression

            if len(parts) == 5:

                left = parts[2]

                right = parts[4]

                if not self.is_number(left):

                    used.add(left)

                if not self.is_number(right):

                    used.add(right)

            # Simple assignment

            elif len(parts) == 3:

                value = parts[2]

                if not self.is_number(value):

                    used.add(value)

            # Conditional jump

            elif (
                len(parts) == 6
                and parts[0] == "if"
            ):

                left = parts[1]

                right = parts[3]

                if not self.is_number(left):

                    used.add(left)

                if not self.is_number(right):

                    used.add(right)
            # PRINT instruction

            elif (
                len(parts) == 2
                and parts[0] == "PRINT"
            ):

                value = parts[1]

                if not self.is_number(value):

                    used.add(value)

        result = []

        for instruction in instructions:

            parts = instruction.split()

            if len(parts) == 3:

                target = parts[0]

                if (
                    self.is_temporary(target)
                    and target not in used
                ):

                    self.stats[
                        "dead_code_elimination"
                    ] += 1

                    continue

            result.append(instruction)

        return result

    # =====================================================
    # STRAIGHT-LINE OPTIMIZATION
    # =====================================================

    def optimize_straight_line(
        self,
        instructions
    ):

        # First fold obvious constants.

        instructions = (
            self.constant_folding(
                instructions
            )
        )

        # Propagate constants.

        instructions = (
            self.constant_propagation(
                instructions
            )
        )

        # Simplify algebra.

        instructions = (
            self.algebraic_simplification(
                instructions
            )
        )

        # CSE BEFORE copy propagation.
        #
        # This is important for:
        #
        # t1 = x + y
        # t2 = x + y
        #
        # becoming:
        #
        # t1 = x + y
        # t2 = t1

        instructions = (
            self.common_subexpression_elimination(
                instructions
            )
        )

        # Propagate copies.

        instructions = (
            self.copy_propagation(
                instructions
            )
        )

        # Fold again after propagation.

        instructions = (
            self.constant_folding(
                instructions
            )
        )

        return instructions

    # =====================================================
    # CONTROL-FLOW REGION SPLITTING
    # =====================================================

    def split_regions(self):

        regions = []

        current = []

        for instruction in self.instructions:

            if self.is_label(instruction):

                if current:

                    regions.append(current)

                    current = []

                regions.append(
                    [instruction]
                )

                continue

            current.append(instruction)

            if (
                self.is_conditional_jump(
                    instruction
                )
                or
                self.is_unconditional_jump(
                    instruction
                )
            ):

                regions.append(current)

                current = []

        if current:

            regions.append(current)

        return regions

    # =====================================================
    # CONTROL-FLOW-SAFE OPTIMIZATION
    # =====================================================

    def optimize_control_flow(
        self
    ):

        regions = self.split_regions()

        result = []

        for region in regions:

            # Label only.

            if (
                len(region) == 1
                and self.is_label(
                    region[0]
                )
            ):

                result.extend(region)

                continue

            # Separate control instructions.

            body = []

            control = []

            for instruction in region:

                if self.is_control_flow(
                    instruction
                ):

                    control.append(
                        instruction
                    )

                else:

                    body.append(
                        instruction
                    )

            # -----------------------------------------
            # Optimize ONLY inside this region.
            # -----------------------------------------

            body = self.constant_folding(
                body
            )

            body = self.constant_propagation(
                body
            )

            body = self.algebraic_simplification(
                body
            )

            # CSE is safe inside a straight-line region.

            body = self.common_subexpression_elimination(
                body
            )

            body = self.copy_propagation(
                body
            )

            body = self.constant_folding(
                body
            )

            result.extend(body)

            result.extend(control)

        return result

    # =====================================================
    # CONTROL FLOW HELPER
    # =====================================================

    def is_control_flow(self, instruction):

        return (
            self.is_label(instruction)
            or
            self.is_conditional_jump(
                instruction
            )
            or
            self.is_unconditional_jump(
                instruction
            )
        )

    # =====================================================
    # MAIN OPTIMIZER
    # =====================================================

    def optimize(self):

        # ---------------------------------------------
        # NO CONTROL FLOW
        # ---------------------------------------------

        if not self.contains_control_flow():

            result = (
                self.optimize_straight_line(
                    self.instructions.copy()
                )
            )

            result = (
                self.dead_code_elimination(
                    result
                )
            )

            return result

        # ---------------------------------------------
        # CONTROL FLOW PRESENT
        # ---------------------------------------------

        result = (
            self.optimize_control_flow()
        )

        # Do NOT run the old global DCE pass here.
        #
        # Control-flow-aware DCE is handled separately
        # by dce.py using liveness analysis.

        return result

    # =====================================================
    # STATISTICS
    # =====================================================

    def get_statistics(self):

        return self.stats.copy()