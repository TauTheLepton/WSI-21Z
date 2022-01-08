from Maze import Maze
from QLearning import QLearning

def readMap(): # TODO read from file (?)
    map = """...#############
...#..S..#..#..#
#..####..#..#..#
#........#.....#
#..#..#..#..#..#
#..#..#.....#..#
#..####..#..####
#..#.F#..#.....#
#..#..#######..#
#.....#.........
#############..."""
    return map

def main():
    M = Maze(readMap())
    shape = M.getMazeSize()
    print(shape)
    print(M.maze)
    print(M.getMoves((0, 0)))
    Q = QLearning(readMap(), 0.1, 0.9)
    print(Q.qtable)

if __name__ == '__main__':
    main()
