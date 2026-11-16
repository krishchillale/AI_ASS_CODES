# Board: a list of 9 cells, like  char board[9]  in C.
# Each cell is 'X', 'O' or ' ' (empty).

INF = 1000      # stands in for infinity


def print_board(board):
    print(" " + board[0] + " | " + board[1] + " | " + board[2])
    print("---+---+---")
    print(" " + board[3] + " | " + board[4] + " | " + board[5])
    print("---+---+---")
    print(" " + board[6] + " | " + board[7] + " | " + board[8])
    print()


# ---------- Who has won? ----------
def check_winner(board):
    lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8],      # rows
             [0, 3, 6], [1, 4, 7], [2, 5, 8],      # columns
             [0, 4, 8], [2, 4, 6]]                 # diagonals

    for line in lines:
        a = line[0]
        b = line[1]
        c = line[2]
        if board[a] != ' ' and board[a] == board[b] and board[b] == board[c]:
            return board[a]          # 'X' or 'O'
    return None                      # nobody yet


def is_full(board):
    for cell in board:
        if cell == ' ':
            return False
    return True


# ---------- Minimax with Alpha-Beta pruning ----------
def minimax(board, depth, alpha, beta, is_maximizing):
    winner = check_winner(board)
    if winner == 'O':
        return 10 - depth            # computer wins (sooner = better)
    if winner == 'X':
        return depth - 10            # human wins
    if is_full(board):
        return 0                     # draw

    if is_maximizing:                # computer's turn (O) wants HIGH score
        best = -INF
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'                                   # make move
                score = minimax(board, depth + 1, alpha, beta, False)
                board[i] = ' '                                   # undo move

                if score > best:
                    best = score
                if best > alpha:
                    alpha = best
                if beta <= alpha:                                # prune
                    break
        return best
    else:                            # human's turn (X) wants LOW score
        best = INF
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, alpha, beta, True)
                board[i] = ' '

                if score < best:
                    best = score
                if best < beta:
                    beta = best
                if beta <= alpha:                                # prune
                    break
        return best


# ---------- Computer chooses its move ----------
def best_move(board):
    best_score = -INF
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, -INF, INF, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    return move


# ---------- Game loop ----------
def play():
    board = [' '] * 9        # nine spaces, like filling a char array with ' '

    print("You are X, the computer is O.")
    print("Cells are numbered 1-9, left to right, top to bottom.\n")
    print_board(board)

    while True:
        # ----- human move -----
        try:
            pos = int(input("Your move (1-9): ")) - 1
        except ValueError:                   # like catching NumberFormatException
            print("Please enter a number from 1 to 9.")
            continue

        if pos < 0 or pos > 8 or board[pos] != ' ':
            print("Invalid move, try again.")
            continue

        board[pos] = 'X'
        print_board(board)

        if check_winner(board) is not None or is_full(board):
            break

        # ----- computer move -----
        move = best_move(board)
        board[move] = 'O'
        print("Computer plays:")
        print_board(board)

        if check_winner(board) is not None or is_full(board):
            break

    winner = check_winner(board)
    if winner is not None:
        print(winner, "wins!")
    else:
        print("It's a draw!")


play()