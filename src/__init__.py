from tkinter import *
from tkinter.filedialog import askopenfilename
from maze import Maze
from node import Node
from os.path import join

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

        leftFrame_title_label = Label(leftFrame_title, text="Maze", justify=CENTER, font="Times 32")
        leftFrame_title_label.pack(pady=(10,0))

        self.canvas = Canvas(leftFrame_title, width=400, height=400)
        self.canvas.pack()

        rightFrame_title_label = Label(rightFrame, text="Options", justify=CENTER, font="Times 32")
        self.select_maze = Button(rightFrame, text="Select Maze", width=20, command=self.maze_selection)
        self.dfs_button = Button(rightFrame, text="Depth First Search", width=20, command=self.apply_dfs)
        self.bfs_button = Button(rightFrame, text="Breadth First Search", width=20)
        self.greedy_button = Button(rightFrame, text="Greedy Best First Search", width=20)
        self.uniform_button = Button(rightFrame, text="Uniform Cost Search", width=20)
        self.iterative_button = Button(rightFrame, text="Iterative Deepining Search", width=20)
        self.a_star_button = Button(rightFrame, text="A* Heuristic Search", width=20)
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

    def maze_selection(self):
        maze_file = askopenfilename()

        if maze_file == "":
            raise ValueError("You have to choose a maze txt file in order to continue...")

        self.maze = Maze(maze_file)

        self.select_maze.configure(state=DISABLED, text="Maze selected")

        self.rectangles = [[] for _ in range(int((len(self.maze.maze_matrix) - 1) / 2))]

        self.fill_canvas()

    def fill_canvas(self):
        row, column = len(self.maze.maze_matrix), len(self.maze.maze_matrix[0])
        matrix = self.maze.maze_matrix
        block_size = 40

        for i in range(1, row, 2):
            real_i = int((i + 1) / 2)
            for j in range(1, column, 2):
                real_j = int((j + 1) / 2)

                self.rectangles[real_i - 1].append(self.canvas.create_rectangle((real_j*block_size), (real_i*block_size), (real_j*block_size + block_size), (real_i*block_size + block_size), fill="white"))

                # if matrix[i][j + 1] == " " and matrix[i+1][j] == " ":

                if matrix[i][j + 1] == "#" and matrix[i+1][j] == " ":
                    #self.canvas.create_rectangle((real_j*block_size), (real_i*block_size), (real_j*block_size + block_size), (real_i*block_size + block_size), fill="white")
                    if j is not (column - 2):
                        self.canvas.create_line((real_j*block_size + block_size), (real_i*block_size), (real_j*block_size + block_size), (real_i*block_size + block_size), width=8)
                if matrix[i][j + 1] == " " and matrix[i+1][j] == "#":
                    #self.canvas.create_rectangle((real_j*block_size), (real_i*block_size), (real_j*block_size + block_size), (real_i*block_size + block_size), fill="white")
                    if i is not (row - 2):
                        self.canvas.create_line((real_j*block_size), (real_i*block_size + block_size), (real_j*block_size + block_size), (real_i*block_size + block_size), width=8)
                if matrix[i][j + 1] == "#" and matrix[i+1][j] == "#":
                    #self.canvas.create_rectangle((real_j*block_size), (real_i*block_size), (real_j*block_size + block_size), (real_i*block_size + block_size), fill="white")
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

        self.canvas.itemconfig(self.rectangles[row - 1][column - 1], fill="blue")

        if self.prev != None:
            self.canvas.itemconfig(self.rectangles[self.prev[0] - 1][self.prev[1] - 1], fill="yellow")
            self.prev = (row, column)
        else:
            self.prev = (row, column)

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

        print("Solution Cost: " + str(dfs.solution_cost), end='\n\n')
        print("Expended Nodes:")
        for i ,n in enumerate(dfs.expanded):
            if i == len(dfs.expanded) - 1:
                print(n)
            else:
                print(n, end=' -> ')

    def reset(self):
        self.enable_buttons()

        self.rectangles = [[] for _ in range(int((len(self.maze.maze_matrix) - 1) / 2))]
        self.prev = None
        self.fill_canvas()

    def disable_buttons(self):
        self.dfs_button.configure(state=DISABLED)
        self.bfs_button.configure(state=DISABLED)
        self.greedy_button.configure(state=DISABLED)
        self.uniform_button.configure(state=DISABLED)
        self.iterative_button.configure(state=DISABLED)
        self.a_star_button.configure(state=DISABLED)

    def enable_buttons(self):
        self.dfs_button.configure(state=NORMAL)
        self.bfs_button.configure(state=NORMAL)
        self.greedy_button.configure(state=NORMAL)
        self.uniform_button.configure(state=NORMAL)
        self.iterative_button.configure(state=NORMAL)
        self.a_star_button.configure(state=NORMAL)


if __name__ == '__main__':
    tk = Tk()
    a = App(tk)
    tk.mainloop()
