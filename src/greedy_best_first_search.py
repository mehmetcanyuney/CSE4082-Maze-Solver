from search_algorithm import SearchAlgorithm
from maze import Maze
import time


class GreedyBestFirstSearch(SearchAlgorithm):
    def search(self):
        while self.frontier is not []:
            # takes the node with minimum heuristic which is calculated when creation of the node
            current_node = self.frontier.pop(self.frontier.index(min(self.frontier, key = lambda x:x.heuristic)))

            # UI related operations
            self.app.update_maze(current_node)
            self.app.root.update()
            time.sleep(self.app.animation_speed)

            # add the node to explored list and its real cordinates to expanded list
            self.explored.append(current_node)
            self.expanded.append((current_node.get_real_coordinates()))

            # check if the current node is goal node or not
            if self.maze[current_node.x][current_node.y] == 'G':
                self.end_node = current_node
                # creating the solution
                self.create_solution()
                break

            # explore all available nodes that is neighboor of given node (current_node)
            explore_result = self.explore(current_node)

            for node in explore_result:
                # if available node is not in frontier and also not in explored list
                if node not in self.frontier and node not in self.explored:
                    self.frontier.append(node)
