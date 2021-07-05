
import string



class Environment:
    def __init__(self) -> None:
        self.env = list(string.ascii_lowercase)
        self.current_index = 0
        
    def move(self, num:int):
        if num > 2 or num < -2:
            raise ValueError('Must be between 2 and -2')

        self.current_index += num

        return self.current_index

    def finished(self):
        return self.env[self.current_index % 26] == 'z'
            

class Node:
    def __init__(self) -> None:
        self.value = 0
        self.num_iterations = 0
        self.children = []

class MCTS:
    def __init__(self, total_iterations=5000) -> None:
        self.total_iterations = total_iterations
        self.root = Node()

    def search(self, current_index):
        for i in range(self.total_iterations):
            node = self.select(self.root)
            self.expand(node)
    

    def expand(self, node):
        node.children.append()

    # getter
    def select(self, node):
        if len(node.children) == 0:
            return node
        
        # need to use uct here
        best_child = node.children[0]
        for child in node.children:
            if child.value > best_child:
                best_child = child
        
        return MCTS.select(best_child)


        


if __name__ == '__main__':
    ts = MCTS()
    env = Environment()
    num_steps = 0
    new_index = 0
    moves = []

    while not env.finished():
        new_index = env.move(ts.search(new_index))
        moves.append(str(new_index))
        num_steps += 1
    
    print(f'Solution found in {num_steps} number of steps')
    print(f'Indices: {" -> ".join(moves)}')
