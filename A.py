GOAL = "123456780"          # '0' is the blank


def heuristic(state):
    count = 0
    for i in range(9):
        if state[i] != '0' and state[i] != GOAL[i]:
            count = count + 1
    return count


def swap_tiles(state, i, j):
    board = list(state)
    temp = board[i]
    board[i] = board[j]
    board[j] = temp
    return ''.join(board)


def get_neighbors(state):
    neighbors = []
    b = state.index('0')
    row = b // 3
    col = b % 3

    if row > 0:
        neighbors.append(swap_tiles(state, b, b - 3))
    if row < 2:
        neighbors.append(swap_tiles(state, b, b + 3))
    if col > 0:
        neighbors.append(swap_tiles(state, b, b - 1))
    if col < 2:
        neighbors.append(swap_tiles(state, b, b + 1))
    return neighbors


def is_solvable(state):
    inversions = 0
    for i in range(9):
        for j in range(i + 1, 9):
            if state[i] != '0' and state[j] != '0' and state[i] > state[j]:
                inversions = inversions + 1
    return inversions % 2 == 0


def print_board(state):
    for i in range(0, 9, 3):
        row = state[i:i + 3].replace('0', '_')
        print(row[0], row[1], row[2])
    print()


# ---------- A* Search ----------
def a_star(start):
    open_list = [start]
    g = {start: 0}               # g[state] = cheapest known moves to reach it
    parent = {start: None}

    while len(open_list) > 0:
        # pick the state with the smallest f = g + h
        best = open_list[0]
        for s in open_list:
            if g[s] + heuristic(s) < g[best] + heuristic(best):
                best = s
        open_list.remove(best)

        # goal reached? rebuild path
        if best == GOAL:
            path = []
            current = best
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path

        for nxt in get_neighbors(best):
            new_g = g[best] + 1                      # each move costs 1
            # new board, OR a shorter route to a known board
            if nxt not in g or new_g < g[nxt]:
                g[nxt] = new_g
                parent[nxt] = best
                if nxt not in open_list:
                    open_list.append(nxt)

    return None


# ---------- Main ----------
start = "813402765"          # 8 1 3 / 4 _ 2 / 7 6 5

print("Start state:")
print_board(start)

if not is_solvable(start):
    print("This puzzle is not solvable.")
else:
    path = a_star(start)
    print("Shortest solution:", len(path) - 1, "moves\n")
    step_no = 0
    for state in path:
        print("Step", step_no)
        print_board(state)
        step_no = step_no + 1