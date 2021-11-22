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
    winner = checkWinner(board, k)
    if winner == 1:
        sum += 5
    elif winner == -1:
        sum -= 5
    return sum

def getBestMove(w, best_moves, max):
    if max:
        best_w = -math.inf
    else:
        best_w = math.inf
    for i in range(len(w)):
        if max:
            if w[i] > best_w:
                best_w = w[i]
                best_move = best_moves[i]
        else:
            if w[i] < best_w:
                best_w = w[i]
                best_move = best_moves[i]
    return best_w, best_move

# returns best move calculated by minimax algorithm
def miniMax(board_original, k, depth, best_eval, best_move, max_turn):
    winner = checkWinner(board_original, k)
    if getMoves(board_original) == []:
        return heuristicsFunction(board_original, k), None # winner, None
    elif winner != 0:
        return heuristicsFunction(board_original, k), None # winner, None
    elif depth == 0:
        return heuristicsFunction(board_original, k), None # 0, None
    moves = getMoves(board_original)
    w = []
    best_moves = []
    for move in moves:
        board = copy.deepcopy(board_original)
        board = makeMove(board, move, max_turn)
        eval, best_move_new = miniMax(board, k, depth-1, best_eval, best_move, not max_turn)
        w.append(eval)
        best_moves.append(move)
    if w != []:
        best_eval, best_move = getBestMove(w, best_moves, max_turn)
    return best_eval, best_move

# returns best move calculated by minimax algorithm with alpha-beta pruning
def miniMaxAlphaBeta(board_original, k, depth, best_move, max_turn, alpha, beta):
    winner = checkWinner(board_original, k)
    if getMoves(board_original) == []:
        return heuristicsFunction(board_original, k), None # winner, None
    elif winner != 0:
        return heuristicsFunction(board_original, k), None # winner, None
    elif depth == 0:
        return heuristicsFunction(board_original, k), None # 0, None
    moves = getMoves(board_original)
    if max_turn:
        for move in moves:
            board = copy.deepcopy(board_original)
            board = makeMove(board, move, max_turn)
            alpha_new, best_move_new = miniMaxAlphaBeta(board, k, depth-1, best_move, not max_turn, alpha, beta)
            if alpha_new > alpha:
                alpha = alpha_new
                best_move = move
            if alpha >= beta:
                return beta, best_move
        return alpha, best_move
    else:
        for move in moves:
            board = copy.deepcopy(board_original)
            board = makeMove(board, move, max_turn)
            beta_new, best_move_new = miniMaxAlphaBeta(board, k, depth-1, best_move, not max_turn, alpha, beta)
            if beta_new < beta:
                beta = beta_new
                best_move = move
            if alpha >= beta:
                return alpha, best_move
        return beta, best_move

# old
# # returns best move calculated by minimax algorithm with alpha-beta pruning
# def miniMaxAlphaBeta(board_original, k, depth, best_move, max_turn, alpha, beta):
#     winner = checkWinner(board_original, k)
#     if winner != 0:
#         return winner, None
#     elif depth == 0:
#         return heuristicsFunction(board_original, k), None # return 0, None
#     board = copy.deepcopy(board_original)
#     if max_turn:
#         moves = getMoves(board)
#         for move in moves:
#             board = makeMove(board, move, True)
#             eval, best_move_new = miniMaxAlphaBeta(board, k, depth-1, best_move, False, alpha, beta)
#             if eval > alpha:
#                 alpha = eval
#                 best_move = move
#             if alpha >= beta:
#                 return beta, best_move
#         return alpha, best_move
#     else:
#         moves = getMoves(board)
#         for move in moves:
#             board = makeMove(board, move, False)
#             eval, best_move_new = miniMaxAlphaBeta(board, k, depth-1, best_move, True, alpha, beta)
#             if eval < beta:
#                 beta = eval
#                 best_move = move
#             if alpha >= beta:
#                 return alpha, best_move
#         return beta, best_move

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
                    eval, move = miniMax(board, k, depth, math.inf, None, 0)
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
                    eval, move = miniMaxAlphaBeta(board, k, depth1, None, player, -math.inf, math.inf)
                else:
                    eval, move = miniMax(board, k, depth1, -math.inf, None, player)
                board = makeMove(board, move, player)
            else:
                if random2:
                    move = randomMove(board)
                elif alpha_beta2:
                    eval, move = miniMaxAlphaBeta(board, k, depth2, None, player, -math.inf, math.inf)
                else:
                    eval, move = miniMax(board, k, depth2, math.inf, None, player)
                board = makeMove(board, move, player)
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
    # board = makeMove(board, (0, 0), 1)
    # board = makeMove(board, (0, 1), 1)
    # board = makeMove(board, (0, 2), 1)
    # print(board)
    # print(checkWinner(board, k))

    # playGame(3, 3, 3, 6, True, False)
    playGameBot(3, 3, 3, 4, True, False, 3, True, False)
    # heuristics = generateHeuristics(5, 5, 4)
    # print(heuristics)

if __name__ == '__main__':
    main()
