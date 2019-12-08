from search_algorithm import SearchAlgorithm
from maze import Maze
import time


class IterativeDeepeningSearch(SearchAlgorithm):
    def search(self):
        start_node = self.frontier.pop()
        self.expanded.append((start_node.get_real_coordinates()))

        max_depth = len(self.maze) * len(self.maze[0])

        for depth in range(max_depth):
            result = self.depthlimitedsearch(start_node, depth)

            if isinstance(result, str):
                pass
            else:
                self.end_node = result
                self.create_solution()
                return "success"
        return "failure"

    def depthlimitedsearch(self, start_node, limit):
        return self.recursive_dls(start_node, limit)

    def recursive_dls(self, node, limit):
        if self.maze[node.x][node.y] == 'G':
            return node
        elif limit == 0:
            return "cutoff"
        else:
            cutoff_occurred = False

            explore_result = self.explore(node)

            for child_node in explore_result:
                if child_node.get_real_coordinates() not in self.expanded:
                    self.expanded.append((child_node.get_real_coordinates()))
                result = self.recursive_dls(child_node, limit - 1)
                if isinstance(result, str):
                    if result == "cutoff":
                        cutoff_occurred = True
                else:
                    return result
            if cutoff_occurred:
                return "cutoff"
            else:
                return "failure"


if __name__ == '__main__':
    maze = Maze("..\\maze\\maze.txt")
    a = IterativeDeepeningSearch(maze=maze)
    if a.search() == 'success':
        print("Solution Path:")
        for i, n in enumerate(a.solution_path):
            if i == len(a.solution_path) - 1:
                print(n, end='\n\n')
            else:
                print(n, end=' -> ')

        print("Solution Cost: " + str(a.solution_cost), end='\n\n')
        print("Expended Nodes:")
        for i ,n in enumerate(a.expanded):
            if i == len(a.expanded) - 1:
                print(n)
            else:
                print(n, end=' -> ')
