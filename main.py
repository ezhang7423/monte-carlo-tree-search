import math
import string
import random


class Environment:
    def __init__(self) -> None:
        self.env = list(string.ascii_lowercase)
        self.current_index = 0

    def move(self, new_index: int):
        num = self.current_index - new_index
        if num > 2 or num < -2:
            raise ValueError("Can only move between 2 and -2 of current index")

        self.current_index = new_index

        return self.current_index

    def finished(self):
        return self.env[self.current_index % 26] == "m"


class Node:
    def __init__(self, move, parent) -> None:
        self.wins = 0
        self.num_iterations = 0
        self.move = move
        self.parent = parent
        self.children = []

    def get_uct(self):
        if self.num_iterations == 0:  # is this ok? maybe not...experiment later
            return math.inf
        else:
            return self.wins / self.num_iterations + 0.9 * math.sqrt(
                math.log(self.parent.num_iterations) / self.num_iterations
            )

    def get_moves(self):
        return {child.move for child in self.children}


class MCTS:
    def __init__(self, current_index, total_iterations=5000) -> None:
        self.total_iterations = total_iterations
        self.root = Node(current_index, None)

    def search(self):
        for i in range(self.total_iterations):
            node = self.select(self.root)
            new_move = self.expand(node)
            val = self.simulate(new_move)
            self.back_prop(val, new_move)

        best_child = self.root.children[0]

        for child in self.root.children:
            if child.get_uct() > best_child.get_uct():
                best_child = child
        return best_child.move

    def back_prop(self, val, node):
        node.wins += val
        node.num_iterations += 1

        if node.parent:
            self.back_prop(val, node.parent)

    def simulate(self, node):
        env = Environment()
        env.current_index = new_index = node.move

        moves = 0
        while moves < 10:
            new_move = random.choice(list(range(-2, 3)))
            new_index += new_move
            env.move(new_index)
            if env.finished():
                return 1
            moves += 1

        return 0  # fail if it takes more than 500 moves

    def expand(self, node):

        new_move = Node(
            random.choice(
                list(
                    {node.move - i for i in range(-2, 3)} - node.get_moves(),
                )
            ),
            node,
        )
        node.children.append(new_move)
        return new_move

    # getter
    def select(self, node):
        if len(node.children) <= 4:  # if this node is not fully expanded yet
            return node

        # # TODO: need to use uct here
        best_child = node.children[0]
        for child in node.children:

            if child.get_uct() > best_child.get_uct():
                best_child = child

        return self.select(best_child)


if __name__ == "__main__":
    env = Environment()
    num_steps = 0
    new_index = 0
    moves = ["0"]

    while not env.finished():
        print("Finding another step...")
        ts = MCTS(
            new_index
        )  # can optimize by retaining tree later...maybe another init func
        new_index = env.move(ts.search())
        moves.append(str(new_index))
        num_steps += 1

    print(f"Solution found in {num_steps} number of steps")
    print(f'Indices: {" -> ".join(moves)}')
