from search_algorithm import SearchAlgorithm
from maze import Maze
import time


class AStarSearch(SearchAlgorithm):
    def search(self):
        while self.frontier is not []:
            current_node = self.frontier.pop(self.frontier.index(min(self.frontier, key = lambda x:x.a_star_heuristic)))

            self.app.update_maze(current_node)
            self.app.root.update()
            time.sleep(self.app.animation_speed)

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
