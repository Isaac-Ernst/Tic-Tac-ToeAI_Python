#
# Tic-Tac-Toe (5/17-19/2023)
# Isaac B. Ernst
#

from copy import deepcopy
from random import randint


puzzle_board = [[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]]

board_index = {1: (0, 0), 2: (0, 1),
               3: (0, 2), 4: (1, 0),
               5: (1, 1), 6: (1, 2),
               7: (2, 0), 8: (2, 1),
               9: (2, 2)}


# Changes color of moves... WORKS!
def print_colored_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"


# Shows the puzzle board... WORKS!
def show_board(board):
    for i in range(len(board)):
        if i in [1, 2]:
            print('=============')
        for j in range(len(board[0])):
            if j in [1, 2]:
                print(' | ', end=' ')
            if j == 2 and type(board[i][j]) != int:
                if board[i][j] == 'X':
                    print(print_colored_text(board[i][j], '31'))
                else:
                    print(print_colored_text(board[i][j], '34'))
            elif j == 2:
                if board[i][j] == 'X':
                    print(print_colored_text(board[i][j], '31'))
                elif board[i][j] == 'O':
                    print(print_colored_text(board[i][j], '34'))
                else:
                    print(board[i][j])
            elif type(board[i][j]) == int:
                print(board[i][j], end=' ')
            else:
                if board[i][j] == 'X':
                    print(print_colored_text(board[i][j], '31'), end=' ')
                else:
                    print(print_colored_text(board[i][j], '34'), end=' ')


# Decides if the user or computer gets the first move... WORKS!
def flip_coin(board):
    print('\nWe will now flip a coin to see who gets the first move.')
    print('Flipping...')
    while True:
        call = input('Heads or Tails? ').lower()
        match call.split():
            case ['head' | 'heads']:
                call = 'heads'
                break
            case ['tail' | 'tails']:
                call = 'tails'
                break
            case _:
                print(f'{call!r} is not a side of the coin!')
    if randint(1, 2) == 1:
        print('Heads won!')
        text1, code1 = 'User', '31'
        text2, code2 = 'Computer', '34'
        p1 = print_colored_text(text1, code1)
        p2 = print_colored_text(text2, code2)
        print(f'{p1} is X\'s & {p2} is O\'s.')
        if call == 'heads':
            show_board(board)
            return True
    else:
        print('Tails won!')
        text1, code1 = 'User', '31'
        text2, code2 = 'Computer', '34'
        p1 = print_colored_text(text1, code1)
        p2 = print_colored_text(text2, code2)
        print(f'{p1} is X\'s & {p2} is O\'s.')
        if call == 'tails':
            show_board(board)
            return True
    return False


# Gets the user's move (always is X's)... WORKS!
def user_move(board, index):
    while True:
        try:
            move = int(input('Enter move (ex: 8): '))
            if move <= 0 or move >= 10:
                print('Invalid input.')
            elif check_move(board, move, index):
                row, col = index[move]
                board[row][col] = 'X'
                break
            else:
                print('Move taken.')
        except (TypeError, IndexError, ValueError):
            print('Invalid input.')


# Evaluate the game state... WORKS!
def evaluate_game_state(board):
    state = check_game(board)
    if state == 'Computer':
        return 1
    elif state == 'User':
        return -1
    else:
        return 0


# Get all moves... WORKS!
def get_all_moves(board):
    temp_set5 = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if type(board[i][j]) == int:
                temp_set5.append((i, j))
    return temp_set5


# Simulates the move... WORKS!
def simulate_move(board, move, max_player):
    temp_board = deepcopy(board)
    row, col = move
    if max_player:
        temp_board[row][col] = 'O'
    else:
        temp_board[row][col] = 'X'
    return temp_board


# Minimax function with alpha/beta pruning... WORKS!
def minimax(board, depth=9, alpha=float('-inf'), beta=float('inf'), max_player=True):
    if depth == 0 or check_game(board):
        return evaluate_game_state(board), None
    best_move = None
    if max_player:
        max_eval = float('-inf')
        for move in get_all_moves(board):
            new_board = simulate_move(board, move, max_player)
            evaluation, _ = minimax(new_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, evaluation)
            if evaluation == max_eval:
                best_move = move
            # alpha = max(max_eval, alpha)
            # if beta <= alpha:
            #     break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in get_all_moves(board):
            new_board = simulate_move(board, move, max_player)
            evaluation, _ = minimax(new_board, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, evaluation)
            if evaluation == min_eval:
                best_move = move
            # beta = min(min_eval, beta)
            # if beta <= alpha:
            #     break
        return min_eval, best_move


# Puts computer's best move on the board... WORKS!
def comp_move(board):
    _, best_move = minimax(board)
    row, col = best_move
    board[row][col] = 'O'


# Checks to make sure the move is not taken... WORKS!
def check_move(board, move, index):
    row, col = index[move]
    for i in range(len(board)):
        for j in range(len(board[0])):
            if type(board[i][j]) != int and (i, j) == (row, col):
                return False
    return True


# Check row... WORKS!
def check_game_row(board):
    for i in range(len(board)):
        if type(board[i]) != int and len(list(set(board[i]))) == 1:
            if 'O' == list(set(board[i]))[0]:
                return 'Computer'
            elif 'X' == list(set(board[i]))[0]:
                return 'User'
            else:
                return False


# Check column... WORKS!
def check_game_col(board):
    for i in range(len(board[0])):
        temp_set = []
        for j in range(len(board[0])):
            temp_set.append(board[j][i])
        if int != type(temp_set) and len(list(set(temp_set))) == 1:
            if 'O' == list(set(temp_set))[0]:
                return 'Computer'
            elif 'X' == list(set(temp_set))[0]:
                return 'User'
            else:
                return False


# Check fist diagonal... WORKS!
def check_game_first_diagonal(board):
    temp_set2 = []
    for i in range(len(board)):
        temp_set2.append(board[i][i])
    if int != type(temp_set2) and len(list(set(temp_set2))) == 1:
        if 'O' == list(set(temp_set2))[0]:
            return 'Computer'
        elif 'X' == list(set(temp_set2))[0]:
            return 'User'
        else:
            return False


# Check second diagonal... WORKS!
def check_game_second_diagonal(board):
    temp_set3 = [board[0][2], board[1][1], board[2][0]]
    if int != type(temp_set3) and len(list(set(temp_set3))) == 1:
        if 'O' == list(set(temp_set3))[0]:
            return 'Computer'
        elif 'X' == list(set(temp_set3))[0]:
            return 'User'
        else:
            return False


# Check empty... WORKS!
def check_game_draw(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if type(board[i][j]) == int:
                return False
    return 'The Cat'


# Checks for winner... WORKS!
def check_game(board):
    check_r = check_game_row(board)
    check_c = check_game_col(board)
    check_1dia = check_game_first_diagonal(board)
    check_2dia = check_game_second_diagonal(board)
    check_d = check_game_draw(board)
    checks = [check_r, check_c, check_1dia, check_2dia, check_d]
    for check in checks:
        if check:
            return check
    return False


# Gets moves until winner is found... WORKS!
def start(board, coin, index):
    if check_game(board):
        print('\nGame over!')
        show_board(board)
        return print(f'{check_game(board)} won!')
    elif coin:
        user_move(board, index)
        if check_game(board):
            print('\nGame over!')
            show_board(board)
            return print(f'{check_game(board)} won!')
        comp_move(board)
        show_board(board)
    else:
        comp_move(board)
        show_board(board)
        if check_game(board):
            print('\nGame over!')
            show_board(board)
            return print(f'{check_game(board)} won!')
        user_move(board, index)
    start(board, coin, index)


# Main function... WORKS!
def main(board, index):
    coin_flip = flip_coin(board)
    start(board, coin_flip, index)


main(puzzle_board, board_index)
