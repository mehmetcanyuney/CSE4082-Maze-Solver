from node import Node

class SearchAlgorithm:
    def __init__(self, maze):
        self.solution_path = []
        self.explored = []
        self.solution_cost = 0

        self.end_node = None

        self.maze = maze.maze_matrix

        # init frontier with current node
        self.frontier = [maze.start]
        self.expanded = [(maze.start.get_real_coordinates())]

    # going to change depending on the algorithm
    def search(self):
        pass

    def check_valid(self, node):
        if self.maze[node.x][node.y] == '#':
            return False
        return True

    def get_cost(self, x, y):
        if self.maze[x][y] == 'T':
            return 7
        else:
            return 1

    def explore(self, node):
        explore_list = []

        x = node.x
        y = node.y

        east  = Node(x, y+1, None)
        south = Node(x+1, y, None)
        west  = Node(x, y-1, None)
        north = Node(x-1, y, None)

        if self.check_valid(east):
            explore_list.append(Node(x, y+2, node, node.cost + self.get_cost(x, y+2)))
        if self.check_valid(south):
            explore_list.append(Node(x+2, y, node, node.cost + self.get_cost(x+2, y)))
        if self.check_valid(west):
            explore_list.append(Node(x, y-2, node, node.cost + self.get_cost(x, y-2)))
        if self.check_valid(north):
            explore_list.append(Node(x-2, y, node, node.cost + self.get_cost(x-2, y)))

        return explore_list

    def create_solution(self):
        temp = self.end_node
        cost = self.end_node.cost
        while temp != None:
            self.solution_path.append((temp.get_real_coordinates()))
            temp = temp.parent

        self.solution_path.reverse()
        self.solution_cost = cost
