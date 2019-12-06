class Node:
    def __init__(self, x, y, parent, cost=1):
        self.x      = x
        self.y      = y
        self.parent = parent
        self.cost   = cost

    def get_real_coordinates(self):
        return int((self.x + 1) / 2), int((self.y + 1) / 2)

    def __eq__(self, equivalent):
        if equivalent == None:
            return False

        is_x_equal = self.x == equivalent.x
        is_y_equal = self.y == equivalent.y

        return is_x_equal and is_y_equal


# checking if __eq__ working or not
if __name__ == '__main__':
    a = Node(5, 5, None, 1)
    b = Node(5, 5, None, 1)
    c = Node(5, 2, None, 1)
    d = Node(5, 5, None, 7)

    list = [a, c, d]

    print(a == b)
    print(a == c)
    print(a == d)

    print(b in list)
