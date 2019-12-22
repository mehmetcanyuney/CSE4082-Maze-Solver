from node import Node

class SearchAlgorithm:
    def __init__(self, app):
        # solution related variables
        self.solution_path = []
        self.explored = []
        self.solution_cost = 0

        # Will be set at the end of the algorithm
        self.end_node = None

        # maze which is given by txt
        self.maze = app.maze.maze_matrix

        # end / goal nodes in order to calculate heuristic
        self.goals = app.maze.maze_goals

        # init frontier with current node
        app.maze.start.heuristic = self.get_manhattan_distance(app.maze.start.x, app.maze.start.y)
        self.frontier = [app.maze.start]

        # expanded list
        self.expanded = []

        # UI elements
        self.app = app

    # going to change depending on the algorithm
    def search(self):
        pass

    # calculates the minimum manhattan distance between goals for given node
    def get_manhattan_distance(self, x, y):
        # getting real distances
        x = int((x + 1) / 2)
        y = int((y + 1) / 2)
        heuristic_results = []
        # calculating each distances to goal nodes
        for n in self.goals:
            n_x, n_y = n.get_real_coordinates()
            heuristic_results.append(abs(x - n_x) + abs(y - n_y))
        # returning the minimum as heuristic value
        return min(heuristic_results)

    # if the element in the matrix is not # which means not wall
    def check_valid(self, node):
        if self.maze[node.x][node.y] == '#':
            return False
        return True

    # if node is empty then cost is 1
    # if node is "T" - trap then cost is 7
    def get_cost(self, x, y):
        if self.maze[x][y] == 'T':
            return 7
        else:
            return 1

    # find the available neighbors
    def explore(self, node):
        # result list
        explore_list = []

        # getting x and y value
        x = node.x
        y = node.y

        # following variables represent the wall / not wall
        # its # then it means wall
        east  = Node(x, y+1, None)
        south = Node(x+1, y, None)
        west  = Node(x, y-1, None)
        north = Node(x-1, y, None)

        # if one of them is avaiable then it returns the actual node (+2)
        # additional informations are given in the documentations
        if self.check_valid(east):
            explore_list.append(Node(x, y+2, node, node.cost + self.get_cost(x, y+2), self.get_manhattan_distance(x, y+2)))
        if self.check_valid(south):
            explore_list.append(Node(x+2, y, node, node.cost + self.get_cost(x+2, y), self.get_manhattan_distance(x+2, y)))
        if self.check_valid(west):
            explore_list.append(Node(x, y-2, node, node.cost + self.get_cost(x, y-2), self.get_manhattan_distance(x, y-2)))
        if self.check_valid(north):
            explore_list.append(Node(x-2, y, node, node.cost + self.get_cost(x-2, y), self.get_manhattan_distance(x-2, y)))

        return explore_list

    # creates the solution solution_path
    # starting from found goal node
    # while loop until the node has no parent which means its start node
    def create_solution(self):
        temp = self.end_node
        cost = self.end_node.cost
        while temp != None:
            self.solution_path.append((temp.get_real_coordinates()))
            temp = temp.parent

        self.solution_path.reverse()
        self.solution_cost = cost
