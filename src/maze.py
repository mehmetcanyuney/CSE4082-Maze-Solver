from os.path import join
from node import Node

class Maze():
    def __init__(self, path=None):
        if path == None:
            raise ValueError("Path cannnot be None")

        # represents the whole maze (walls included) with a matrix
        self.maze_matrix = []
        self.maze_goals = []

        with open(path, 'r') as file:
            for i, line in enumerate(file):
                line = list(line[:-1])
                self.maze_matrix.append(line)

                # Assigns the starting node
                if 'S' in line:
                    self.start = Node(i, line.index('S'), None, cost=0)

                # Assigns the goal nodes
                g_temp = [index for index, value in enumerate(line) if value == 'G']

                for index in g_temp:
                    self.maze_goals.append(Node(i, index, None, cost=0))

if __name__ == '__main__':
    m = Maze(path=join("..", "maze", "maze.txt"))
    print(m.start.x)
    print(m.start.y)
    print(m.start.get_real_coordinates())
    print()
    for i in m.maze_goals:
        print(i.get_real_coordinates())
