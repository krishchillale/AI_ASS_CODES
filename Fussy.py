ROWS = 5
COLS = 5

# '#' = ink, '.' = empty.  Think of each one as a char[5][5] in C.
TEMPLATES = {
    'I': [".###.",
          "..#..",
          "..#..",
          "..#..",
          ".###."],
    'L': ["#....",
          "#....",
          "#....",
          "#....",
          "#####"],
    'T': ["#####",
          "..#..",
          "..#..",
          "..#..",
          "..#.."],
    'O': [".###.",
          "#...#",
          "#...#",
          "#...#",
          ".###."],
    'X': ["#...#",
          ".#.#.",
          "..#..",
          ".#.#.",
          "#...#"],
    'H': ["#...#",
          "#...#",
          "#####",
          "#...#",
          "#...#"],
}


# ---------- Step 1: picture (text) -> crisp grid of 1.0 / 0.0 ----------
def to_crisp(rows):
    grid = []
    for r in range(ROWS):
        line = []
        for c in range(COLS):
            if rows[r][c] == '#':
                line.append(1.0)
            else:
                line.append(0.0)
        grid.append(line)
    return grid


# ---------- Step 2: FUZZIFICATION (the membership function) ----------
#   ink cell                   -> 1.0
#   empty cell touching ink    -> 0.5
#   empty cell far from ink    -> 0.0
def fuzzify(crisp):
    fuzzy = []
    for r in range(ROWS):
        line = []
        for c in range(COLS):
            if crisp[r][c] == 1.0:
                line.append(1.0)
            else:
                near_ink = False
                for dr in (-1, 0, 1):             # look at all 8 neighbours
                    for dc in (-1, 0, 1):
                        nr = r + dr
                        nc = c + dc
                        if 0 <= nr < ROWS and 0 <= nc < COLS:
                            if crisp[nr][nc] == 1.0:
                                near_ink = True
                if near_ink:
                    line.append(0.5)
                else:
                    line.append(0.0)
        fuzzy.append(line)
    return fuzzy


# ---------- Step 3: fuzzy similarity  = sum(min) / sum(max) ----------
def similarity(a, b):
    top = 0.0
    bottom = 0.0
    for r in range(ROWS):
        for c in range(COLS):
            top = top + min(a[r][c], b[r][c])         # fuzzy intersection
            bottom = bottom + max(a[r][c], b[r][c])   # fuzzy union
    if bottom == 0:
        return 0.0
    return top / bottom


def print_fuzzy(fuzzy):
    for r in range(ROWS):
        print("  ".join("%.1f" % v for v in fuzzy[r]))
    print()


# ---------- Build the fuzzy version of every template once ----------
fuzzy_templates = {}
for name in TEMPLATES:
    fuzzy_templates[name] = fuzzify(to_crisp(TEMPLATES[name]))


# ---------- Step 4: compare input with every template ----------
def recognize(rows):
    f_in = fuzzify(to_crisp(rows))
    best_name = None
    best_score = -1.0
    for name in fuzzy_templates:
        score = similarity(f_in, fuzzy_templates[name])
        print("  %s : %.2f" % (name, score))
        if score > best_score:
            best_score = score
            best_name = name
    return best_name, best_score


# ---------- Main: messy "handwritten" test inputs ----------
tests = {
    "T with a missing pixel": ["####.",
                               "..#..",
                               "..#..",
                               "..#..",
                               "..#.."],
    "O with a gap":           [".###.",
                               "#...#",
                               "#....",
                               "#...#",
                               ".###."],
    "L with a noise dot":     ["#....",
                               "#....",
                               "#..#.",
                               "#....",
                               "#####"],
    "X written wobbly":       ["#...#",
                               ".#.#.",
                               "..#..",
                               ".#...",
                               "#...#"],
    "H with a broken leg":    ["#...#",
                               "#...#",
                               "#####",
                               "#...#",
                               "#...."],
    "T shifted down":         [".....",
                               "#####",
                               "..#..",
                               "..#..",
                               "..#.."],
}

print("Fuzzy membership grid of template 'T':\n")
print_fuzzy(fuzzy_templates['T'])

for title in tests:
    print("Input:", title)
    name, score = recognize(tests[title])
    print("  => Recognized as '%s' (similarity %.2f)\n" % (name, score))