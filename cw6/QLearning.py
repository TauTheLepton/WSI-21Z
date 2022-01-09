import numpy as np
from random import randrange
from Maze import Maze

class QLearning:
    def __init__(self, maze_map, alpha, discount):
        """
        qtable[actions][names]
        """
        self.actions = ['start', 'idle', 'correct', 'wrong', 'end']
        self.names = ['down', 'right', 'up', 'left']
        self.qtable = self.makeQTable()
        self.maze = Maze(maze_map)
        self.alpha = alpha
        self.state = 0 # TODO
        self.discount = discount

    def makeQTable(self):
        # subtable = {name: 0.0 for name in self.names}
        # table = {action: subtable.copy() for action in self.actions}
        table = np.zeros((len(self.actions), len(self.names)))
        return table

    def checkReward(self):
        rewards = {}
        for name in self.names:
            move = self.maze.checkMove(name)
            if move == None:
                value = -100
            elif self.maze.checkIfWon():
                value = 100
            elif self.maze.isRightWay(name):
                value = 1
            else:
                value = -1
            rewards[name] = value
        return rewards

    def updateTable(self, name, new_state):
        temp = self.checkReward()[name] + self.discount * max(self.qtable[new_state, :]) - self.qtable[self.state][name]
        self.qtable[self.state][name] = self.qtable[self.state][name] + self.alpha * temp

    def chooseMove(self):
        action_values = []
        names = []
        for action_value, name in zip(self.qtable[self.state, :], self.names):
            if action_value == max(self.qtable[self.state, :]):
                action_values.append(action_value)
                names.append(name)
        if len(action_values) > 1:
            idx = randrange(len(action_values))
        else:
            idx = 0
        return action_values[idx], names[idx]

    def getMoveAndNewState(self):
        action_value, name = self.chooseMove()
        move = self.maze.checkMove(name)
        if move == None:
            if self.state == 0:
                new_state = 0
            else:
                new_state = 1
        else:
            if self.maze.isRightWay(name):
                new_state = 2
            else:
                new_state = 3
            if move == self.maze.finish:
                new_state = 4
        return move, name, new_state

    def learn(self):
        move, name, new_state = self.getMoveAndNewState()
        self.updateTable(name, new_state)
        self.maze.makeMove(move)
        if self.maze.checkIfWon():
            pass # TODO idk, add some ending or sth
