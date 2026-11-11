# MiniTAC Compiler
# Data Flow Analysis
#
# Implements live variable analysis on basic blocks.


class LivenessAnalyzer:

    def __init__(self, cfg):

        self.cfg = cfg

        # IN[B] = variables live before block B
        self.live_in = {}

        # OUT[B] = variables live after block B
        self.live_out = {}

        # Variables defined inside each block
        self.definitions = {}

        # Variables used inside each block
        self.uses = {}

    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(self):

        self.calculate_use_def()

        # Initialize sets

        for block in self.cfg.blocks:

            self.live_in[block.block_id] = set()

            self.live_out[block.block_id] = set()

        changed = True

        # Repeat until the sets stop changing.

        while changed:

            changed = False

            # Liveness is a backward data-flow analysis,
            # so process blocks from the end toward the start.

            for block in reversed(
                self.cfg.blocks
            ):

                block_id = block.block_id

                old_in = self.live_in[
                    block_id
                ].copy()

                old_out = self.live_out[
                    block_id
                ].copy()

                # -----------------------------------------
                # OUT[B] =
                # union of IN of all successors
                # -----------------------------------------

                new_out = set()

                for successor in block.successors:

                    new_out.update(
                        self.live_in[
                            successor.block_id
                        ]
                    )

                # -----------------------------------------
                # IN[B] =
                # USE[B] ∪ (OUT[B] - DEF[B])
                # -----------------------------------------

                new_in = (
                    self.uses[block_id]
                    |
                    (
                        new_out
                        -
                        self.definitions[block_id]
                    )
                )

                self.live_out[block_id] = new_out

                self.live_in[block_id] = new_in

                if (
                    old_in != new_in
                    or old_out != new_out
                ):

                    changed = True

        return self.live_in, self.live_out

    # =====================================================
    # CALCULATE USE / DEF
    # =====================================================

    def calculate_use_def(self):

        for block in self.cfg.blocks:

            definitions = set()

            uses = set()

            for instruction in (
                block.instructions
            ):

                parts = instruction.split()

                # =========================================
                # LABEL
                #
                # L1:
                # =========================================

                if (
                    len(parts) == 1
                    and parts[0].endswith(":")
                ):

                    continue

                # =========================================
                # CONDITIONAL JUMP
                #
                # if a > b goto L1
                #
                # parts:
                # [if, a, >, b, goto, L1]
                # =========================================

                if (
                    len(parts) == 6
                    and parts[0] == "if"
                    and parts[4] == "goto"
                ):

                    left = parts[1]

                    right = parts[3]

                    if (
                        not self.is_number(left)
                        and left not in definitions
                    ):

                        uses.add(left)

                    if (
                        not self.is_number(right)
                        and right not in definitions
                    ):

                        uses.add(right)

                    continue

                # =========================================
                # UNCONDITIONAL JUMP
                #
                # goto L1
                # =========================================

                if (
                    len(parts) == 2
                    and parts[0] == "goto"
                ):

                    continue

                # =========================================
                # BINARY INSTRUCTION
                #
                # t1 = a + b
                #
                # parts:
                # [t1, =, a, +, b]
                # =========================================

                if len(parts) == 5:

                    result = parts[0]

                    left = parts[2]

                    right = parts[4]

                    if (
                        not self.is_number(left)
                        and left not in definitions
                    ):

                        uses.add(left)

                    if (
                        not self.is_number(right)
                        and right not in definitions
                    ):

                        uses.add(right)

                    definitions.add(result)

                    continue

                # =========================================
                # SIMPLE ASSIGNMENT
                #
                # b = a
                #
                # parts:
                # [b, =, a]
                # =========================================

                if len(parts) == 3:

                    result = parts[0]

                    value = parts[2]

                    if (
                        not self.is_number(value)
                        and value not in definitions
                    ):

                        uses.add(value)

                    definitions.add(result)

            self.definitions[
                block.block_id
            ] = definitions

            self.uses[
                block.block_id
            ] = uses

    # =====================================================
    # CHECK NUMBER
    # =====================================================

    def is_number(self, value):

        return value.lstrip("-").isdigit()

    # =====================================================
    # DISPLAY ANALYSIS
    # =====================================================

    def display(self):

        print("=" * 60)
        print("LIVENESS ANALYSIS")
        print("=" * 60)

        for block in self.cfg.blocks:

            block_id = block.block_id

            print()
            print(block_id)

            print(
                "    USE : "
                + self.format_set(
                    self.uses[block_id]
                )
            )

            print(
                "    DEF : "
                + self.format_set(
                    self.definitions[block_id]
                )
            )

            print(
                "    IN  : "
                + self.format_set(
                    self.live_in[block_id]
                )
            )

            print(
                "    OUT : "
                + self.format_set(
                    self.live_out[block_id]
                )
            )

    # =====================================================
    # FORMAT SET
    # =====================================================

    def format_set(self, values):

        if not values:

            return "{}"

        return (
            "{"
            + ", ".join(sorted(values))
            + "}"
        )