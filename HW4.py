import math


def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    return None


def empty_cells(board):
    cells = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                cells.append((i, j))
    return cells


def evaluate(board):
    winner = check_winner(board)
    if winner == 'X':
        return 1
    elif winner == 'O':
        return -1
    else:
        return 0


def make_move(board, player, row, col):
    board[row][col] = player


def minimax(board, depth, alpha, beta, is_maximizing):
    score = evaluate(board)

    if score == 1 or score == -1:
        return score

    if len(empty_cells(board)) == 0:
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for cell in empty_cells(board):
            row, col = cell
            make_move(board, 'X', row, col)
            eval = minimax(board, depth + 1, alpha, beta, False)
            make_move(board, ' ', row, col)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for cell in empty_cells(board):
            row, col = cell
            make_move(board, 'O', row, col)
            eval = minimax(board, depth + 1, alpha, beta, True)
            make_move(board, ' ', row, col)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def find_best_move(board):
    best_eval = -math.inf
    best_move = (-1, -1)
    for cell in empty_cells(board):
        row, col = cell
        make_move(board, 'X', row, col)
        eval = minimax(board, 0, -math.inf, math.inf, False)
        make_move(board, ' ', row, col)
        if eval > best_eval:
            best_eval = eval
            best_move = (row, col)
    return best_move


def display_board(board):
    print(" " + board[0][0] + " | " + board[0][1] + " | " + board[0][2])
    print("-----------")
    print(" " + board[1][0] + " | " + board[1][1] + " | " + board[1][2])
    print("-----------")
    print(" " + board[2][0] + " | " + board[2][1] + " | " + board[2][2])
    print()


def play_game():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    player_first = input("Player first? (yes/no): ").lower().strip() == 'yes'

    while True:
        display_board(board)
        if player_first:
            row, col = map(int, input("Input your turn (<row> <column>): ").split())
            make_move(board, 'O', row - 1, col - 1)
        else:
            row, col = find_best_move(board)
            make_move(board, 'X', row, col)

        winner = check_winner(board)
        if winner:
            display_board(board)
            if winner == 'X':
                print("AI wins!")
            else:
                print("Player wins!")
            break

        if len(empty_cells(board)) == 0:
            display_board(board)
            print("No winner!")
            break

        player_first = not player_first


play_game()