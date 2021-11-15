import numpy as np

class Game:

    def __init__(self, n, m, k):
        self.n = n
        self.m = m
        self.board = np.zeros((n, m), dtype=int)
        self.k = k

    def makeMove(self, max_move, move):
        (x, y) = move
        if max_move:
            self.board[x][y] = 1
        else:
            self.board[x][y] = -1
    
    def getSize(self):
        return self.n, self.m
    
    def getMove(self):
        possible_moves = []
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] == 0:
                    possible_moves.append((i, j))
        return possible_moves
    
    def isOver(self):
        is_over = False
        winner = None
        for i in range(self.n):
            for j in range(self.m):
                status = True
                if self.board[i][j] != 0:
                    if i <= self.n - self.k:
                        for k in range(self.k):
                            if self.board[i + k][j] != self.board[i][j]: status = False
                        if status: winner = self.board[i][j]
                        else: status = True
                    if j <= self.m - self.k:
                        for k in range(self.k):
                            if self.board[i][j + k] != self.board[i][j]: status = False
                        if status: winner = self.board[i][j]
                        else: status = True
                    if i <= self.n - self.k and j <= self.m - self.k:
                        for k in range(self.k):
                            if self.board[i + k][j + k] != self.board[i][j]: status = False
                        if status: winner = self.board[i][j]
        if winner != None: is_over = True
        return is_over, winner

class ArtificialIntelligence:
    def __init__(self, d, cutting, random):
        self.d = d
        self.cut = cutting
        self.rand = random

def main():
    g = Game(5, 5, 3)
    g.makeMove(1, (1, 2))
    g.makeMove(1, (3, 3))
    g.makeMove(1, (3, 4))
    print(g.board)
    print(g.isOver())

if __name__ == '__main__':
    main()
