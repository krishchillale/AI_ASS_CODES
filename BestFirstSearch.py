GOAL = "123456780"          # '0' is the blank


# ---------- Heuristic: count misplaced tiles ----------
def heuristic(state):
    count = 0
    for i in range(9):
        if state[i] != '0' and state[i] != GOAL[i]:   # ignore the blank
            count = count + 1
    return count


# ---------- Swap two positions in a state ----------
def swap_tiles(state, i, j):
    board = list(state)          # string -> list so we can modify it
    temp = board[i]
    board[i] = board[j]
    board[j] = temp
    return ''.join(board)        # list -> string again


# ---------- All states reachable in one move ----------
def get_neighbors(state):
    neighbors = []
    b = state.index('0')         # position of the blank
    row = b // 3
    col = b % 3

    if row > 0:                  # blank can move up
        neighbors.append(swap_tiles(state, b, b - 3))
    if row < 2:                  # blank can move down
        neighbors.append(swap_tiles(state, b, b + 3))
    if col > 0:                  # blank can move left
        neighbors.append(swap_tiles(state, b, b - 1))
    if col < 2:                  # blank can move right
        neighbors.append(swap_tiles(state, b, b + 1))
    return neighbors


# ---------- Is the puzzle solvable? (inversion count must be even) ----------
def is_solvable(state):
    inversions = 0
    for i in range(9):
        for j in range(i + 1, 9):
            if state[i] != '0' and state[j] != '0' and state[i] > state[j]:
                inversions = inversions + 1
    return inversions % 2 == 0


# ---------- Print a board nicely ----------
def print_board(state):
    for i in range(0, 9, 3):                       # i = 0, 3, 6
        row = state[i:i + 3].replace('0', '_')     # show blank as _
        print(row[0], row[1], row[2])
    print()


# ---------- Best First Search ----------
def best_first_search(start):
    open_list = [start]          # states waiting to be explored
    parent = {start: None}       # like a HashMap: state -> where we came from

    while len(open_list) > 0:
        # find the state in open_list with the smallest heuristic
        best = open_list[0]
        for s in open_list:
            if heuristic(s) < heuristic(best):
                best = s
        open_list.remove(best)

        # goal reached? rebuild the path by following parents backwards
        if best == GOAL:
            path = []
            current = best
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path

        # otherwise add unseen neighbors to the open list
        for nxt in get_neighbors(best):
            if nxt not in parent:        # not visited yet
                parent[nxt] = best
                open_list.append(nxt)

    return None                          # no solution found


# ---------- Main ----------
start = "123406758"

print("Start state:")
print_board(start)

if not is_solvable(start):
    print("This puzzle is not solvable.")
else:
    path = best_first_search(start)
    print("Solved in", len(path) - 1, "moves\n")
    step_no = 0
    for state in path:
        print("Step", step_no)
        print_board(state)
        step_no = step_no + 1