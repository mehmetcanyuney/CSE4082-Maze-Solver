from tkinter import *
from tkinter.filedialog import askopenfilename
from maze import Maze
from node import Node
from os.path import join
import time

# Algorithms
from depth_first_search import DepthFirstSearch
from breadth_first_search import BreadthFirstSearch
from greedy_best_first_search import GreedyBestFirstSearch
from uniform_cost_search import UniformCostSearch
from iterative_deepening_search import IterativeDeepeningSearch
from a_star_search import AStarSearch


class App:
    def __init__(self, root):
        self.root = root

        self.root.title("Search Algorithm Benchmarker")
        self.root.iconbitmap(join("..", "templates", "benchmark.ico"))

        self.maze = None

        self.rectangles = None
        self.prev = None
        self.prev_node = None

        self.animation_speed = 0.2

        windowWidth = 600
        windowHeight = 450
        positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
        root.geometry("{}x{}+{}+{}".format(windowWidth,windowHeight,positionRight, positionDown))

        leftFrame = Frame(self.root)
        leftFrame.pack(side=LEFT, fill=BOTH)
        rightFrame = Frame(self.root)
        rightFrame.pack(side=RIGHT, fill=BOTH)

        leftFrame_title = Frame(leftFrame)
        leftFrame_title.pack(side=TOP)

        leftFrame_title_label = Label(leftFrame_title, text="Maze", justify=CENTER, font="Times 32 italic bold")
        leftFrame_title_label.pack(pady=(10,0))

        self.canvas = Canvas(leftFrame_title, width=400, height=400)
        self.canvas.pack()

        rightFrame_title_label = Label(rightFrame, text="Options", justify=CENTER, font="Times 32 italic bold")
        self.select_maze = Button(rightFrame, text="Select Maze", width=20, command=self.maze_selection)
        self.dfs_button = Button(rightFrame, text="Depth First Search", width=20, command=self.apply_dfs)
        self.bfs_button = Button(rightFrame, text="Breadth First Search", width=20, command=self.apply_bfs)
        self.greedy_button = Button(rightFrame, text="Greedy Best First Search", width=20, command=self.apply_gbfs)
        self.uniform_button = Button(rightFrame, text="Uniform Cost Search", width=20, command=self.apply_uniform)
        self.iterative_button = Button(rightFrame, text="Iterative Deepining Search", width=20, command=self.apply_ids)
        self.a_star_button = Button(rightFrame, text="A* Heuristic Search", width=20, command=self.apply_astar)
        self.reset_button = Button(rightFrame, text="Reset", width=20, command=self.reset)

        rightFrame_title_label.grid(row=0, column=0, pady=(10,0), padx=(0,100))
        self.select_maze.grid(row = 1, column = 0, pady=(20,0), padx=(0,100))
        self.dfs_button.grid(row = 2, column = 0, pady=(20,0), padx=(0,100))
        self.bfs_button.grid(row = 3, column = 0, pady=(20,0), padx=(0,100))
        self.iterative_button.grid(row = 4, column = 0, pady=(20,0), padx=(0,100))
        self.uniform_button.grid(row = 5, column = 0, pady=(20,0), padx=(0,100))
        self.greedy_button.grid(row = 6, column = 0, pady=(20,0), padx=(0,100))
        self.a_star_button.grid(row = 7, column = 0, pady=(20,0), padx=(0,100))
        self.reset_button.grid(row = 8, column = 0, pady=(20,0), padx=(0,100))

        self.disable_buttons()

    # maze selection function in order to get txt file from user
    def maze_selection(self):
        maze_file = askopenfilename()

        if maze_file == "":
            raise ValueError("You have to choose a maze txt file in order to continue...")

        self.maze = Maze(maze_file)

        self.select_maze.configure(state=DISABLED, text="Maze selected")

        self.rectangles = [[] for _ in range(int((len(self.maze.maze_matrix) - 1) / 2))]

        self.fill_canvas()
        self.enable_buttons()

    # fill the canvas that contains the maze
    def fill_canvas(self):
        row, column = len(self.maze.maze_matrix), len(self.maze.maze_matrix[0])
        matrix = self.maze.maze_matrix
        block_size = 40

        for i in range(1, row, 2):
            real_i = int((i + 1) / 2)
            for j in range(1, column, 2):
                real_j = int((j + 1) / 2)

                self.rectangles[real_i - 1].append(self.canvas.create_rectangle((real_j*block_size), (real_i*block_size), (real_j*block_size + block_size), (real_i*block_size + block_size), fill="white"))

                if matrix[i][j + 1] == "#" and matrix[i+1][j] == " ":
                    if j is not (column - 2):
                        self.canvas.create_line((real_j*block_size + block_size), (real_i*block_size), (real_j*block_size + block_size), (real_i*block_size + block_size), width=8)
                if matrix[i][j + 1] == " " and matrix[i+1][j] == "#":
                    if i is not (row - 2):
                        self.canvas.create_line((real_j*block_size), (real_i*block_size + block_size), (real_j*block_size + block_size), (real_i*block_size + block_size), width=8)
                if matrix[i][j + 1] == "#" and matrix[i+1][j] == "#":
                    if j is not (column - 2):
                        self.canvas.create_line((real_j*block_size + block_size), (real_i*block_size), (real_j*block_size + block_size), (real_i*block_size + block_size), width=8)
                    if i is not (row - 2):
                        self.canvas.create_line((real_j*block_size), (real_i*block_size + block_size), (real_j*block_size + block_size), (real_i*block_size + block_size), width=8)

                if matrix[i][j] == 'S':
                    self.canvas.create_text((real_j*block_size + int(block_size / 2)), (real_i*block_size + int(block_size / 2)), text="S", font="Times 30", fill="black")
                if matrix[i][j] == 'G':
                    self.canvas.create_text((real_j*block_size + int(block_size / 2)), (real_i*block_size + int(block_size / 2)), text="G", font="Times 30", fill="green")
                if matrix[i][j] == 'T':
                    self.canvas.create_text((real_j*block_size + int(block_size / 2)), (real_i*block_size + int(block_size / 2)), text="T", font="Times 30", fill="red")

        self.canvas.create_line((block_size),(block_size),(int((column + 1) / 2) * block_size),(block_size), width=5)
        self.canvas.create_line((block_size),(block_size),(block_size),(int((row + 1) / 2) * block_size), width=5)
        self.canvas.create_line((block_size),(int((row + 1) / 2) * block_size),(int((column + 1) / 2) * block_size),(int((row + 1) / 2) * block_size), width=5)
        self.canvas.create_line((int((column + 1) / 2) * block_size),(block_size),(int((column + 1) / 2) * block_size),(int((row + 1) / 2) * block_size), width=5)

    def update_maze(self, node):
        row, column = node.get_real_coordinates()

        if self.prev != None:
            self.canvas.itemconfig(self.rectangles[self.prev[0] - 1][self.prev[1] - 1], fill="yellow")
            self.prev = (row, column)
        else:
            self.prev = (row, column)

        self.canvas.itemconfig(self.rectangles[row - 1][column - 1], fill="blue")

    # update maze with colors
    # special case for dfs because it requires to go back when it has no where to go/
    def update_maze_dfs_special(self, node):
        row, column = node.get_real_coordinates()

        if self.prev_node != None:
            if self.prev_node != node.parent:
                temp_prev = self.prev_node
                while node.parent != temp_prev:
                    i, j = temp_prev.get_real_coordinates()
                    self.canvas.itemconfig(self.rectangles[i - 1][j - 1], fill="yellow")
                    i, j = temp_prev.parent.get_real_coordinates()
                    self.canvas.itemconfig(self.rectangles[i - 1][j - 1], fill="blue")
                    self.root.update()
                    temp_prev = temp_prev.parent
                    time.sleep(self.animation_speed)
                i, j = node.parent.get_real_coordinates()
                self.canvas.itemconfig(self.rectangles[i - 1][j - 1], fill="yellow")
                self.prev_node = node
                self.root.update()
            else:
                i, j = self.prev_node.get_real_coordinates()
                self.canvas.itemconfig(self.rectangles[i - 1][j - 1], fill="yellow")
                self.prev_node = node
                self.root.update()
        else:
            self.prev_node = node

        self.canvas.itemconfig(self.rectangles[row - 1][column - 1], fill="blue")
        self.root.update()

    def apply_dfs(self):
        self.disable_buttons()

        dfs = DepthFirstSearch(app=self)

        dfs.search()

        print("Solution Path:")
        for i ,n in enumerate(dfs.solution_path):
            if i == len(dfs.solution_path) - 1:
                print(n, end='\n\n')
            else:
                print(n, end=' -> ')

        self.update_solution_on_canvas(dfs.solution_path)

        print("Solution Cost: " + str(dfs.solution_cost), end='\n\n')
        print("Expended Nodes:")
        for i ,n in enumerate(dfs.expanded):
            if i == len(dfs.expanded) - 1:
                print(n)
            else:
                print(n, end=' -> ')

        self.reset_button.configure(state=NORMAL)

    def apply_bfs(self):
        self.disable_buttons()

        bfs = BreadthFirstSearch(app=self)

        bfs.search()

        print("Solution Path:")
        for i ,n in enumerate(bfs.solution_path):
            if i == len(bfs.solution_path) - 1:
                print(n, end='\n\n')
            else:
                print(n, end=' -> ')

        self.update_solution_on_canvas(bfs.solution_path)

        print("Solution Cost: " + str(bfs.solution_cost), end='\n\n')
        print("Expended Nodes:")
        for i ,n in enumerate(bfs.expanded):
            if i == len(bfs.expanded) - 1:
                print(n)
            else:
                print(n, end=' -> ')

        self.reset_button.configure(state=NORMAL)

    def apply_gbfs(self):
        self.disable_buttons()

        gbfs = GreedyBestFirstSearch(app=self)

        gbfs.search()

        print("Solution Path:")
        for i ,n in enumerate(gbfs.solution_path):
            if i == len(gbfs.solution_path) - 1:
                print(n, end='\n\n')
            else:
                print(n, end=' -> ')

        self.update_solution_on_canvas(gbfs.solution_path)

        print("Solution Cost: " + str(gbfs.solution_cost), end='\n\n')
        print("Expended Nodes:")
        for i ,n in enumerate(gbfs.expanded):
            if i == len(gbfs.expanded) - 1:
                print(n)
            else:
                print(n, end=' -> ')

        self.reset_button.configure(state=NORMAL)

    def apply_astar(self):
        self.disable_buttons()

        astar = AStarSearch(app=self)

        astar.search()

        print("Solution Path:")
        for i ,n in enumerate(astar.solution_path):
            if i == len(astar.solution_path) - 1:
                print(n, end='\n\n')
            else:
                print(n, end=' -> ')

        self.update_solution_on_canvas(astar.solution_path)

        print("Solution Cost: " + str(astar.solution_cost), end='\n\n')
        print("Expended Nodes:")
        for i ,n in enumerate(astar.expanded):
            if i == len(astar.expanded) - 1:
                print(n)
            else:
                print(n, end=' -> ')

        self.reset_button.configure(state=NORMAL)

    def apply_uniform(self):
        self.disable_buttons()

        uniform = UniformCostSearch(app=self)

        uniform.search()

        print("Solution Path:")
        for i ,n in enumerate(uniform.solution_path):
            if i == len(uniform.solution_path) - 1:
                print(n, end='\n\n')
            else:
                print(n, end=' -> ')

        self.update_solution_on_canvas(uniform.solution_path)

        print("Solution Cost: " + str(uniform.solution_cost), end='\n\n')
        print("Expended Nodes:")
        for i ,n in enumerate(uniform.expanded):
            if i == len(uniform.expanded) - 1:
                print(n)
            else:
                print(n, end=' -> ')

        self.reset_button.configure(state=NORMAL)

    def apply_ids(self):
        self.disable_buttons()

        ids = IterativeDeepeningSearch(app=self)

        ids.search()

        print("Solution Path:")
        for i ,n in enumerate(ids.solution_path):
            if i == len(ids.solution_path) - 1:
                print(n, end='\n\n')
            else:
                print(n, end=' -> ')

        self.update_solution_on_canvas(ids.solution_path)

        print("Solution Cost: " + str(ids.solution_cost), end='\n\n')
        print("Expended Nodes:")
        for i ,n in enumerate(ids.expanded):
            if i == len(ids.expanded) - 1:
                print(n)
            else:
                print(n, end=' -> ')

        self.reset_button.configure(state=NORMAL)

    def reset(self):
        self.enable_buttons()

        self.rectangles = [[] for _ in range(int((len(self.maze.maze_matrix) - 1) / 2))]
        self.prev = None
        self.prev_node = None
        self.fill_canvas()

    def disable_buttons(self):
        self.dfs_button.configure(state=DISABLED)
        self.bfs_button.configure(state=DISABLED)
        self.greedy_button.configure(state=DISABLED)
        self.uniform_button.configure(state=DISABLED)
        self.iterative_button.configure(state=DISABLED)
        self.a_star_button.configure(state=DISABLED)
        self.reset_button.configure(state=DISABLED)

    def enable_buttons(self):
        self.dfs_button.configure(state=NORMAL)
        self.bfs_button.configure(state=NORMAL)
        self.greedy_button.configure(state=NORMAL)
        self.uniform_button.configure(state=NORMAL)
        self.iterative_button.configure(state=NORMAL)
        self.a_star_button.configure(state=NORMAL)

        self.reset_button.configure(state=DISABLED)

    def update_solution_on_canvas(self, solution_path):
        for i, j in solution_path:
            self.canvas.itemconfig(self.rectangles[i - 1][j - 1], fill="DeepSkyBlue3")
        self.root.update()


if __name__ == '__main__':
    tk = Tk()
    a = App(tk)
    tk.mainloop()
