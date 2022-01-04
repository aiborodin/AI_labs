from heapq import heappush, heappop
from copy import deepcopy


class GameState:
    def __init__(self, board, parent=None):
        self.board = board
        self.parent = parent
        self.heuristic_score = None
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1

    def __eq__(self, other):
        return self.board == other.board

    def __lt__(self, other):
        return self.heuristic_score < other.heuristic_score

    def __hash__(self):
        return hash(str(self.board))

    def __str__(self):
        return '\n'.join(' '.join(str(el) if el is not None else ' ' for el in row) for row in self.board)

    def get_board(self):
        return self.board

    def calc_heuristic_score(self, target):
        self.heuristic_score = self.count_misplaced(target) + self.parent.depth + 1

    def count_misplaced(self, target):
        misplaced = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != target.board[i][j]:
                    misplaced += 1
        return misplaced

    def descendants(self):
        desc = []
        i, j = self.find_none_indexes()
        if (i - 1) >= 0:
            board = deepcopy(self.board)
            board[i][j] = board[i - 1][j]
            board[i - 1][j] = None
            desc.append(GameState(board, self))
        if (i + 1) < len(self.board):
            board = deepcopy(self.board)
            board[i][j] = board[i + 1][j]
            board[i + 1][j] = None
            desc.append(GameState(board, self))
        if (j - 1) >= 0:
            board = deepcopy(self.board)
            board[i][j] = board[i][j - 1]
            board[i][j - 1] = None
            desc.append(GameState(board, self))
        if (j + 1) < len(self.board):
            board = deepcopy(self.board)
            board[i][j] = board[i][j + 1]
            board[i][j + 1] = None
            desc.append(GameState(board, self))
        return desc

    def find_none_indexes(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] is None:
                    return [i, j]

    def path_from_root(self):
        path = []
        curr_node = self
        while curr_node is not None:
            path.append(curr_node)
            curr_node = curr_node.parent
        path.reverse()
        return path


def a_star_search(start: GameState, target: GameState):
    opened = []
    closed = set()
    heappush(opened, start)
    while opened:
        current = heappop(opened)
        if current == target:
            return current.path_from_root()
        closed.add(current)
        for desc in current.descendants():
            if desc not in opened and desc not in closed:
                desc.calc_heuristic_score(target)
                heappush(opened, desc)
    return None


def get_start(i):
    return [
        GameState([
            [2, 8, 3],
            [1, 6, 4],
            [7, None, 5]
        ]),
        GameState([
            [7, 2, 4],
            [None, 3, 5],
            [6, 8, 1]
        ]),
    ][i]


def get_target():
    return GameState([
        [1, 2, 3],
        [8, None, 4],
        [7, 6, 5]
    ])


def print_path(path):
    path_len = len(path)
    print("Number of steps: ", path_len-1)
    for i in range(3):
        for j in range(path_len):
            board = path[j].get_board()
            if i == 1 and j != path_len-1:
                print(' '.join(str(el) if el is not None else ' ' for el in board[i]), end=' --> ')
            else:
                print(' '.join(str(el) if el is not None else ' ' for el in board[i]), end='     ')
        print('')


path_from_root = a_star_search(get_start(1), get_target())
print_path(path_from_root)



