from Maze import Maze
from QLearning import QLearning

small_map = """....
.S#.
.##.
..F."""

big_map = """...#############
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

def main():
    global small_map, big_map

    # set here map and number of iterations to use
    map_to_use = small_map
    iterations = 10 ** 4

    M = Maze(map_to_use)
    print(M.maze)
    Q = QLearning(map_to_use, 0.1, 0.9)
    Q.learn(iterations)
    for item in Q.maze_history:
        print(item)
    print(M.maze)

if __name__ == '__main__':
    main()
