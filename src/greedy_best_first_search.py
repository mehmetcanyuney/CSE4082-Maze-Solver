from search_algorithm import SearchAlgorithm
from maze import Maze
import time


class GreedyBestFirstSearch(SearchAlgorithm):
    def search(self):
        while self.frontier is not []:
            current_node = self.frontier.pop(self.frontier.index(min(self.frontier, key = lambda x:x.heuristic)))

            self.app.update_maze(current_node)
            self.app.root.update()
            time.sleep(0.5)
            # input()

            self.explored.append(current_node)
            self.expanded.append((current_node.get_real_coordinates()))

            if self.maze[current_node.x][current_node.y] == 'G':
                self.end_node = current_node
                self.create_solution()
                break

            explore_result = self.explore(current_node)

            for node in explore_result:
                if node not in self.frontier and node not in self.explored:
                    self.frontier.append(node)


if __name__ == '__main__':
    maze = Maze("..\\maze\\maze.txt")
    a = GreedyBestFirstSearch(maze=maze)
    a.search()
    print("Solution Path:")
    for i ,n in enumerate(a.solution_path):
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
