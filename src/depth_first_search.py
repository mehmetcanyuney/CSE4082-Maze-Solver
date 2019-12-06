from search_algorithm import SearchAlgorithm
from queue import Queue
from maze import Maze

class DepthFirstSearch(SearchAlgorithm):
    def search(self):
        while self.frontier is not []:
            current_node = self.frontier.pop()

            real_x, real_y = current_node.get_real_coordinates()
            # print("Popped : " + str(real_x) + " - " + str(real_y))
            # input()

            self.explored.append(current_node)

            if self.maze[current_node.x][current_node.y] == 'G':
                self.end_node = current_node
                self.create_solution()
                break

            explore_result = self.explore(current_node)

            for node in reversed(explore_result):
                if node not in self.frontier and node not in self.explored:
                    self.frontier.append(node)
                    self.expanded.append((node.get_real_coordinates()))


if __name__ == '__main__':
    maze = Maze("..\\maze\\maze.txt")
    a = DepthFirstSearch(maze=maze)
    a.search()
    print(a.solution_path)
    print(a.solution_cost)
    print(a.expanded)
