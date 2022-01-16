import numpy as np

class Maze:
    def __init__(self, maze):
        """
        maze: string with visual representation of maze, walls are '#', free cells are '.', start is 'S' and finish is 'F'
        """
        self.maze = np.array(self.makeMaze(maze))
        self.position = self.getStartPos()
        self.historical_positions = [self.position]
        self.finish = self.getFinishPos()

    def makeMaze(self, maze_str):
        maze = [[]]
        idx = 0
        for sign in maze_str:
            if sign == '\n':
                idx += 1
                maze.append([])
            else:
                maze[idx].append(sign)
        return maze

    def getMoves(self, pos_now):
        """
        return: dict[pos] = name
        dictionary with keys of positions and values of names for these moves
        """
        positions = self.generatePositions(pos_now)
        moves = {}
        for pos, name in positions.items():
            if self.isPosEmpty(pos):
                moves[pos] = name
        return moves

    def generatePositions(self, pos):
        positions = [
            (pos[0] + 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] - 1),
        ]
        names = ['down', 'right', 'up', 'left']
        my_dict = {}
        for position, name in zip(positions, names):
            if position[0] < self.maze.shape[0] and position[1] < self.maze.shape[1] and position[0] >= 0 and position[1] >= 0: # check if (x, y) is inside maze
                my_dict[position] = name
        return my_dict

    def isPosEmpty(self, pos):
        if self.maze[pos[0]][pos[1]] == '#':
            return False
        else:
            return True

    def getMazeSize(self):
        """
        return: tuple with X-axis and Y-axis size of maze
        """
        return self.maze.shape

    def getStartPos(self):
        """
        return: tuple with start position
        """
        for x in range(self.getMazeSize()[0]):
            for y in range(self.getMazeSize()[1]):
                if self.maze[x][y] == 'S':
                    return (x, y)

    def getFinishPos(self):
        """
        return: tuple with finish position
        """
        for x in range(self.getMazeSize()[0]):
            for y in range(self.getMazeSize()[1]):
                if self.maze[x][y] == 'F':
                    return (x, y)

    def checkIfWon(self):
        """
        return: bool with True if is on final position
        """
        if self.maze[self.position[0]][self.position[1]] == 'F':
            return True
        else:
            return False

    def makeMove(self, pos):
        """
        pos: tuple with position to move
        if this position is empty move there and add this move to history
        """
        if pos == None:
            # situation when wants to move into wall, so move can't happen
            return False
        elif self.isPosEmpty(pos):
            self.position = pos
            self.historical_positions.append(pos)
            return True
        else:
            return False

    def checkMove(self, move_name, pos=None):
        """
        takes name of move and checks if there is such move possible, if yes returns it, else returns None
        if pos is None checks current position, alse checks given position
        """
        if pos == None:
            moves = self.getMoves(self.position)
        else:
            moves = self.getMoves(pos)
        for move_loop, move_name_loop in moves.items():
            if move_name_loop == move_name:
                return move_loop
        return None

    def calcDistance(self):
        return abs(self.position[0] - self.finish[0]) + abs(self.position[1] - self.finish[1])

    def isRightWay(self, name):
        if self.position[0] < self.finish[0]:
            if name == 'down':
                return True
            elif name == 'up':
                return False
        elif self.position[0] > self.finish[0]:
            if name == 'down':
                return False
            elif name == 'up':
                return True
        elif self.position[1] < self.finish[1]:
            if name == 'right':
                return True
            elif name == 'left':
                return False
        elif self.position[1] > self.finish[1]:
            if name == 'right':
                return False
            elif name == 'left':
                return True
        return None

    def startFromBegining(self):
        historical_positions = self.historical_positions
        self.position = self.getStartPos()
        self.historical_positions = []
        return historical_positions
