# MiniTAC Compiler
# Control Flow Graph
#
# This module:
# 1. Finds leaders in TAC
# 2. Builds basic blocks
# 3. Creates edges between blocks


class BasicBlock:

    def __init__(self, block_id):

        self.block_id = block_id

        self.instructions = []

        self.successors = []

        self.predecessors = []

    def add_instruction(self, instruction):

        self.instructions.append(instruction)

    def __repr__(self):

        return f"BasicBlock({self.block_id})"


class ControlFlowGraph:

    def __init__(self, instructions):

        self.instructions = instructions

        self.blocks = []

        self.label_to_block = {}

    # =====================================================
    # BUILD CFG
    # =====================================================

    def build(self):

        if not self.instructions:

            return self.blocks

        leaders = self.find_leaders()

        self.create_basic_blocks(leaders)

        self.create_edges()

        return self.blocks

    # =====================================================
    # FIND LEADERS
    #
    # A leader is:
    #
    # 1. First instruction
    # 2. Target of a jump
    # 3. Instruction immediately after a jump
    # =====================================================

    def find_leaders(self):

        leaders = set()

        # First instruction is always a leader.

        leaders.add(0)

        # Map labels to instruction indexes.

        label_indexes = {}

        for index, instruction in enumerate(
            self.instructions
        ):

            if instruction.endswith(":"):

                label = instruction[:-1]

                label_indexes[label] = index

        # ---------------------------------------------
        # Find jumps
        # ---------------------------------------------

        for index, instruction in enumerate(
            self.instructions
        ):

            parts = instruction.split()

            # Conditional jump:
            #
            # if a > b goto L1

            if (
                len(parts) == 6
                and parts[0] == "if"
                and parts[4] == "goto"
            ):

                target = parts[5]

                if target in label_indexes:

                    leaders.add(
                        label_indexes[target]
                    )

                # Instruction after conditional jump

                if index + 1 < len(
                    self.instructions
                ):

                    leaders.add(index + 1)

            # Unconditional jump:
            #
            # goto L1

            elif (
                len(parts) == 2
                and parts[0] == "goto"
            ):

                target = parts[1]

                if target in label_indexes:

                    leaders.add(
                        label_indexes[target]
                    )

                # Instruction after jump

                if index + 1 < len(
                    self.instructions
                ):

                    leaders.add(index + 1)

        return sorted(leaders)

    # =====================================================
    # CREATE BASIC BLOCKS
    # =====================================================

    def create_basic_blocks(self, leaders):

        self.blocks = []

        # Each leader starts a new block.

        for i, leader in enumerate(leaders):

            # End of this block

            if i + 1 < len(leaders):

                end = leaders[i + 1]

            else:

                end = len(
                    self.instructions
                )

            block = BasicBlock(
                f"B{i + 1}"
            )

            for index in range(
                leader,
                end
            ):

                block.add_instruction(
                    self.instructions[index]
                )

            self.blocks.append(block)

        # ---------------------------------------------
        # Map labels to blocks
        # ---------------------------------------------

        for block in self.blocks:

            for instruction in block.instructions:

                if instruction.endswith(":"):

                    label = instruction[:-1]

                    self.label_to_block[
                        label
                    ] = block

    # =====================================================
    # CREATE CFG EDGES
    # =====================================================

    def create_edges(self):

        for i, block in enumerate(
            self.blocks
        ):

            if not block.instructions:

                continue

            last = block.instructions[-1]

            parts = last.split()

            # ---------------------------------------------
            # Conditional jump
            #
            # if a > b goto L1
            # ---------------------------------------------

            if (
                len(parts) == 6
                and parts[0] == "if"
                and parts[4] == "goto"
            ):

                target = parts[5]

                target_block = (
                    self.label_to_block.get(
                        target
                    )
                )

                if target_block is not None:

                    self.add_edge(
                        block,
                        target_block
                    )

                # Fall-through block

                if i + 1 < len(
                    self.blocks
                ):

                    self.add_edge(
                        block,
                        self.blocks[i + 1]
                    )

            # ---------------------------------------------
            # Unconditional jump
            #
            # goto L1
            # ---------------------------------------------

            elif (
                len(parts) == 2
                and parts[0] == "goto"
            ):

                target = parts[1]

                target_block = (
                    self.label_to_block.get(
                        target
                    )
                )

                if target_block is not None:

                    self.add_edge(
                        block,
                        target_block
                    )

            # ---------------------------------------------
            # Normal instruction
            #
            # Fall through to next block
            # ---------------------------------------------

            else:

                if i + 1 < len(
                    self.blocks
                ):

                    self.add_edge(
                        block,
                        self.blocks[i + 1]
                    )

    # =====================================================
    # ADD EDGE
    # =====================================================

    def add_edge(
        self,
        source,
        destination
    ):

        if destination not in source.successors:

            source.successors.append(
                destination
            )

        if source not in destination.predecessors:

            destination.predecessors.append(
                source
            )

    # =====================================================
    # DISPLAY CFG
    # =====================================================

    def display(self):

        for block in self.blocks:

            print("=" * 60)

            print(
                f"{block.block_id}"
            )

            print("=" * 60)

            for instruction in (
                block.instructions
            ):

                print(
                    f"    {instruction}"
                )

            successors = [
                successor.block_id
                for successor
                in block.successors
            ]

            predecessors = [
                predecessor.block_id
                for predecessor
                in block.predecessors
            ]

            print()

            print(
                "Successors: "
                + (
                    ", ".join(successors)
                    if successors
                    else "None"
                )
            )

            print(
                "Predecessors: "
                + (
                    ", ".join(predecessors)
                    if predecessors
                    else "None"
                )
            )

            print()