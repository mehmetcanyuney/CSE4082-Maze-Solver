from search_algorithm import SearchAlgorithm
from maze import Maze
import time


class BreadthFirstSearch(SearchAlgorithm):
    def search(self):
        while self.frontier is not []:
            # takes the first element of the frontier and adds them in normal order
            # Frontier is FIFO
            current_node = self.frontier.pop(0)

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
                self.create_solution()
                break

            # explore all available nodes that is neighboor of given node (current_node)
            explore_result = self.explore(current_node)

            for node in explore_result:
                # if available node is not in frontier and also not in explored list
                if node not in self.frontier and node not in self.explored:
                    self.frontier.append(node)
