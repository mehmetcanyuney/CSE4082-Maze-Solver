from search_algorithm import SearchAlgorithm
from maze import Maze
import time


class IterativeDeepeningSearch(SearchAlgorithm):
    def search(self):
        # Popping the only node which is starting node from frontier
        start_node = self.frontier.pop()

        # calculating maximum number of movement and assign this number as max_depth
        max_depth = len(self.maze) * len(self.maze[0])

        # calling the Depth Limited Search with depth limit (from 0 to max_depth)
        for depth in range(max_depth):
            result = self.depthlimitedsearch(start_node, depth)
            # if DLS cannot find the goal node or stuck at depth limit
            if isinstance(result, str):
                pass
            else:
                self.end_node = result
                self.create_solution()
                return "success"
        return "failure"

    def depthlimitedsearch(self, node, limit):
        # adding the current node to expanded list
        self.expanded.append((node.get_real_coordinates()))
        self.app.update_maze(node)
        self.app.root.update()
        # visiting a lot of nodes so animation speed increased
        time.sleep(self.app.animation_speed / 16)

        # exit if the algorithm finds the goal node
        if self.maze[node.x][node.y] == 'G':
            return node
        # stuck at depth limit
        elif limit == 0:
            return "cutoff"
        else:
            # explore available nodes
            explore_result = self.explore(node)

            # check every neighboor
            for child_node in explore_result:
                # passing the neighboor if the neigboor / child is the parent node's itself.
                if child_node == node.parent:
                    continue
                # recursive call of DLS
                result = self.depthlimitedsearch(child_node, limit - 1)
                if isinstance(result, str):
                    pass
                else:
                    return result
            return "cutoff"
