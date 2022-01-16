from Maze import Maze
from QLearning import QLearning

def readSimpleMap():
    map = """....
.S#.
.##.
..F."""
    return map

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
    # set here map and number of iterations to use
    map = readSimpleMap()
    iterations = 10 ** 6

    M = Maze(map)
    print(M.maze)
    Q = QLearning(map, 0.1, 0.9)
    Q.learn(iterations)
    for item in Q.maze_history:
        print(item)
    print(M.maze)

if __name__ == '__main__':
    main()
