# MiniTAC Compiler
# Liveness-Based Dead Code Elimination
#
# Uses the CFG and liveness information to remove
# assignments to temporaries whose values are never used.


class DeadCodeEliminator:

    def __init__(self, cfg, analyzer):

        self.cfg = cfg

        self.analyzer = analyzer

        self.removed_count = 0

    # =====================================================
    # RUN DEAD CODE ELIMINATION
    # =====================================================

    def eliminate(self):

        optimized_blocks = []

        for block in self.cfg.blocks:

            live = set(
                self.analyzer.live_out[
                    block.block_id
                ]
            )

            new_instructions = []

            # Work backwards through the block.

            for instruction in reversed(
                block.instructions
            ):

                parts = instruction.split()

                # -----------------------------------------
                # LABEL
                # -----------------------------------------

                if (
                    len(parts) == 1
                    and parts[0].endswith(":")
                ):

                    new_instructions.append(
                        instruction
                    )

                    continue

                # -----------------------------------------
                # CONDITIONAL JUMP
                #
                # if a > b goto L1
                # -----------------------------------------

                if (
                    len(parts) == 6
                    and parts[0] == "if"
                    and parts[4] == "goto"
                ):

                    left = parts[1]

                    right = parts[3]

                    self.add_use(
                        live,
                        left
                    )

                    self.add_use(
                        live,
                        right
                    )

                    new_instructions.append(
                        instruction
                    )

                    continue

                # -----------------------------------------
                # UNCONDITIONAL JUMP
                # -----------------------------------------

                if (
                    len(parts) == 2
                    and parts[0] == "goto"
                ):

                    new_instructions.append(
                        instruction
                    )

                    continue
                # -----------------------------------------
                # PRINT
                #
                # PRINT t1
                # -----------------------------------------

                if (
                    len(parts) == 2
                    and parts[0] == "PRINT"
                ):

                    value = parts[1]

    # PRINT uses this value, so it must
    # remain live.

                    self.add_use(
                    live,
                    value
                )

                new_instructions.append(
                    instruction
                )

                continue

                # -----------------------------------------
                # BINARY ASSIGNMENT
                #
                # t1 = a + b
                # -----------------------------------------

                if len(parts) == 5:

                    result = parts[0]

                    left = parts[2]

                    right = parts[4]

                    # If the result is a temporary and
                    # nobody needs it afterward, remove it.

                    if (
                        self.is_temporary(result)
                        and result not in live
                    ):

                        self.removed_count += 1

                        # Do NOT add its operands to live
                        # because the instruction disappears.

                        continue

                    # Otherwise the instruction remains.

                    new_instructions.append(
                        instruction
                    )

                    # The result is now defined.

                    live.discard(result)

                    # Its operands are needed before this
                    # instruction.

                    self.add_use(
                        live,
                        left
                    )

                    self.add_use(
                        live,
                        right
                    )

                    continue

                # -----------------------------------------
                # SIMPLE ASSIGNMENT
                #
                # t1 = a
                # -----------------------------------------

                if len(parts) == 3:

                    result = parts[0]

                    value = parts[2]

                    if (
                        self.is_temporary(result)
                        and result not in live
                    ):

                        self.removed_count += 1

                        continue

                    new_instructions.append(
                        instruction
                    )

                    live.discard(result)

                    self.add_use(
                        live,
                        value
                    )

                    continue

                # Unknown instruction:
                # keep it safely.

                new_instructions.append(
                    instruction
                )

            new_instructions.reverse()

            optimized_blocks.append(
                (
                    block,
                    new_instructions
                )
            )

        return optimized_blocks

    # =====================================================
    # CHECK TEMPORARY
    # =====================================================

    def is_temporary(self, value):

        return (
            value.startswith("t")
            and value[1:].isdigit()
        )

    # =====================================================
    # ADD VARIABLE TO LIVE SET
    # =====================================================

    def add_use(self, live, value):

        if value.lstrip("-").isdigit():

            return

        if value.startswith("L"):

            return

        live.add(value)

    # =====================================================
    # GET REMOVAL COUNT
    # =====================================================

    def get_removed_count(self):

        return self.removed_count

    # =====================================================
    # GET OPTIMIZED TAC
    # =====================================================

    def get_optimized_tac(
        self,
        optimized_blocks
    ):

        instructions = []

        for block, block_instructions in (
            optimized_blocks
        ):

            instructions.extend(
                block_instructions
            )

        return instructions