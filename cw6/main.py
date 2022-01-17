from Maze import Maze
from QLearning import QLearning
from matplotlib import pyplot as plt

small_map = """....
.S#.
.##.
..F."""

medium_map3 = """..#####
..#.S.#
#.#.###
#.....#
#.#####
#...F..
#####.."""

medium_map4 = """..#######
..#.S.#.#
#.#.###.#
#.......#
#####.###
#.#.....#
#.###.###
#.....F..
#######.."""

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

def plotLength(lists):
    lengths = [len(list_one) for list_one in lists]
    plt.plot(lengths)
    plt.show()

def main():
    global small_map, big_map,medium_map3, medium_map4

    # set here map and number of iterations to use
    map_to_use = medium_map3
    iterations = 10 ** 6

    M = Maze(map_to_use)
    # print(M.maze)
    Q = QLearning(map_to_use, 0.1, 0.9)
    Q.learn(iterations)
    # for item in Q.maze_history:
    #     print(item)
    # print('-----')
    print(min(Q.maze_history, key=len))
    print(M.maze)
    plotLength(Q.maze_history)

if __name__ == '__main__':
    main()
