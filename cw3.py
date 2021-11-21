import numpy as np
import random
import math
import copy

# creates board of giver dimensions
def makeBoard(n, m):
    return np.zeros((n, m), dtype=int)

# performs move by the selected player
def makeMove(board, move, max_move):
    (x, y) = move
    if max_move:
        board[x][y] = 1
    else:
        board[x][y] = -1
    return board

# returns list of all possible moves
def getMoves(board):
    (n, m) = board.shape
    possible_moves = []
    for i in range(n):
        for j in range(m):
            if board[i][j] == 0:
                possible_moves.append((i, j))
    return possible_moves

# returns '1' or '-1' respectively if either player won and '0' if neither did
def checkWinner(board, k):
    (n, m) = board.shape
    # print(n, m)
    winner = 0
    for i in range(n):
        for j in range(m):
            status = True
            if board[i][j] != 0:
                if i <= n - k:
                    for kk in range(k):
                        if board[i + kk][j] != board[i][j]: status = False
                    if status: winner = board[i][j]
                    else: status = True
                if j <= m - k:
                    for kk in range(k):
                        if board[i][j + kk] != board[i][j]: status = False
                    if status: winner = board[i][j]
                    else: status = True
                if i <= n - k and j <= m - k:
                    for kk in range(k):
                        if board[i + kk][j + kk] != board[i][j]: status = False
                    if status: winner = board[i][j]
                    else: status = True
    for i in range(n-k+1):
        for j in range(k-1,m):
            status = True
            if board[i][j] != 0:
                for kk in range(k):
                    if board[i + kk][j - kk] != board[i][j]: status = False
                if status: winner = board[i][j]
    return winner

# generates table with heuristics values for tic-tac-toe of given size
def generateHeuristics(n, m, k):
    board = makeBoard(n, m)
    for i in range(n):
        for j in range(m):
                if i <= n - k:
                    for kk in range(k):
                        board[i + kk][j] += 1
                if j <= m - k:
                    for kk in range(k):
                        board[i][j + kk] += 1
                if i <= n - k and j <= m - k:
                    for kk in range(k):
                        board[i + kk][j + kk] += 1
    for i in range(n-k+1):
        for j in range(k-1,m):
            for kk in range(k):
                board[i + kk][j - kk] += 1
    return board

# calculates value of heuristics function for given state of the game
def heuristicsFunction(board, k):
    (n, m) = board.shape
    heuristics = generateHeuristics(n, m, k)
    sum = 0
    for i in range(n):
        for j in range(m):
            sum += heuristics[i][j] * board[i][j]
    return sum

# returns best move calculated by minimax algorithm
def miniMax(board_original, k, depth, best_eval, best_move, max_turn):
    winner = checkWinner(board_original, k)
    if winner != 0:
        return winner, None
    elif depth == 0:
        return heuristicsFunction(board_original, k), None # return 0, None
    board = copy.deepcopy(board_original)
    if max_turn:
        best_eval = -math.inf
        moves = getMoves(board)
        for move in moves:
            board = makeMove(board, move, True)
            eval, best_move_new = miniMax(board, k, depth-1, best_eval, best_move, False)
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_eval, best_move
    else:
        best_eval = math.inf
        moves = getMoves(board)
        for move in moves:
            board = makeMove(board, move, False)
            eval, best_move_new = miniMax(board, k, depth-1, best_eval, best_move, True)
            if eval < best_eval:
                best_eval = eval
                best_move = move
        return best_eval, best_move

# returns best move calculated by minimax algorithm with alpha-beta pruning
def miniMaxAlphaBeta(board_original, k, depth, best_move, max_turn, alpha, beta):
    winner = checkWinner(board_original, k)
    if winner != 0:
        return winner, None
    elif depth == 0:
        return heuristicsFunction(board_original, k), None # return 0, None
    board = copy.deepcopy(board_original)
    if max_turn:
        moves = getMoves(board)
        for move in moves:
            board = makeMove(board, move, True)
            eval, best_move_new = miniMaxAlphaBeta(board, k, depth-1, best_move, False, alpha, beta)
            if eval > alpha:
                alpha = eval
                best_move = move
            if alpha >= beta:
                return beta, best_move
        return alpha, best_move
    else:
        moves = getMoves(board)
        for move in moves:
            board = makeMove(board, move, False)
            eval, best_move_new = miniMaxAlphaBeta(board, k, depth-1, best_move, True, alpha, beta)
            if eval < beta:
                beta = eval
                best_move = move
            if alpha >= beta:
                return alpha, best_move
        return beta, best_move

# returns random move from the ones available
def randomMove(board):
    moves = getMoves(board)
    move_idx = random.randrange(1, len(moves))
    return moves[move_idx]

# plays the game with human in command line
def playGame(n, m, k, depth, alpha_beta, random):
    player = None
    while player != "y" and player != "n":
        player = input("Do you want to start? [y/n] ")
    if player == "y": player = True
    else: player = False
    print("You play as '1' against '-1'")
    board = makeBoard(n, m)
    for i in range(n*m):
        if checkWinner(board, k) == 0:
            print("----------")
            if player:
                moves = getMoves(board)
                for j in range(len(moves)):
                    print("move", j, ":", moves[j])
                move = input("Your move: ")
                move = int(move)
                board = makeMove(board, moves[move], 1)
            else:
                if random:
                    move = randomMove(board)
                elif alpha_beta:
                    eval, move = miniMaxAlphaBeta(board, k, depth, None, 0, -math.inf, math.inf)
                else:
                    eval, move = miniMax(board, k, depth, 0, None, 0)
                board = makeMove(board, move, 0)
            print(board)
            player = not player
        else:
            break
    print("Game over!")
    print("The winner is: ", checkWinner(board, k))

# plays the game bot vs bot with different params
def playGameBot(n, m, k, depth1, alpha_beta1, random1, depth2, alpha_beta2, random2):
    player = True
    board = makeBoard(n, m)
    for i in range(n*m):
        if checkWinner(board, k) == 0:
            print("----------") # let's see the game
            if player:
                if random1:
                    move = randomMove(board)
                elif alpha_beta1:
                    eval, move = miniMaxAlphaBeta(board, k, depth1, None, 1, -math.inf, math.inf)
                else:
                    eval, move = miniMax(board, k, depth2, 0, None, 1)
                board = makeMove(board, move, 1)
            else:
                if random2:
                    move = randomMove(board)
                elif alpha_beta2:
                    eval, move = miniMaxAlphaBeta(board, k, depth2, None, 0, -math.inf, math.inf)
                else:
                    eval, move = miniMax(board, k, depth2, 0, None, 0)
                board = makeMove(board, move, 0)
            print(board) # let's see the game
            player = not player
        else:
            break
    print("Game over!") # let's see the game
    print("The winner is: ", checkWinner(board, k)) # let's see the game

def main():
    # board = makeBoard(3, 3)
    # k=3
    # # moves = getMoves(board)
    # # print(board)
    # # print(moves)
    # # eval, move = miniMax(board, k, 6, 0, None, True)
    # # print(eval, move)
    # board = makeMove(board, (1, 0), 1)
    # board = makeMove(board, (1, 1), 1)
    # board = makeMove(board, (1, 2), 1)
    # print(board)
    # print(checkWinner(board, k))

    # playGame(3, 3, 3, 6, True, False)
    playGameBot(3, 3, 3, 3, False, False, 3, True, False)
    # heuristics = generateHeuristics(3, 3, 3)
    # print(heuristics)

if __name__ == '__main__':
    main()
