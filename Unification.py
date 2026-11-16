# ------------------------------------------------------------
# How terms are written:
#   variable        ->  string starting with '?'      e.g. '?x'
#   constant        ->  plain string                  e.g. 'John'
#   predicate/func  ->  list: [name, arg1, arg2, ...] e.g. ['Loves', 'John', '?x']
#   negated literal ->  predicate name starts with '~' e.g. ['~Human', '?x']
# ------------------------------------------------------------

def is_variable(t):
    return isinstance(t, str) and t.startswith('?')     # like instanceof in Java


def is_compound(t):
    return isinstance(t, list)


# ---------- Printing helpers ----------
def term_to_string(t):
    if is_compound(t):
        args = []
        for a in t[1:]:                  # t[1:] = everything after the name
            args.append(term_to_string(a))
        return t[0] + "(" + ", ".join(args) + ")"
    return t


# ---------- Apply a substitution to a term ----------
def apply_subst(t, subst):
    if is_variable(t):
        if t in subst:
            return apply_subst(subst[t], subst)
        return t
    if is_compound(t):
        result = []
        for part in t:
            result.append(apply_subst(part, subst))
        return result
    return t


# ---------- Occurs check: is var hiding inside t?  (stops ?x = f(?x)) ----------
def occurs(var, t, subst):
    if var == t:
        return True
    if is_variable(t) and t in subst:
        return occurs(var, subst[t], subst)
    if is_compound(t):
        for part in t:
            if occurs(var, part, subst):
                return True
    return False


# ---------- Bind a variable to a term ----------
def unify_var(var, x, subst):
    if var in subst:
        return unify(subst[var], x, subst)
    if is_variable(x) and x in subst:
        return unify(var, subst[x], subst)
    if occurs(var, x, subst):
        return None                      # None means FAIL (like null)
    new_subst = dict(subst)              # copy the HashMap
    new_subst[var] = x
    return new_subst


# ---------- THE UNIFICATION ALGORITHM ----------
def unify(x, y, subst):
    if subst is None:                    # an earlier step already failed
        return None
    if x == y:                           # identical, nothing to do
        return subst
    if is_variable(x):
        return unify_var(x, y, subst)
    if is_variable(y):
        return unify_var(y, x, subst)
    if is_compound(x) and is_compound(y):
        if len(x) != len(y):             # different number of arguments
            return None
        for i in range(len(x)):          # unify name, then each argument
            subst = unify(x[i], y[i], subst)
            if subst is None:
                return None
        return subst
    return None                          # two different constants


def show_subst(subst):
    if subst is None:
        return "FAIL (not unifiable)"
    if len(subst) == 0:
        return "{} (already identical)"
    parts = []
    for v in subst:
        parts.append(v + " / " + term_to_string(apply_subst(v, subst)))
    return "{ " + ", ".join(parts) + " }"


# ================= RESOLUTION PART =================

# Give variables a unique suffix so two clauses never clash
def rename(t, suffix):
    if is_variable(t):
        return t + suffix
    if is_compound(t):
        result = []
        for part in t:
            result.append(rename(part, suffix))
        return result
    return t


def clause_to_string(clause):
    if len(clause) == 0:
        return "[] (empty clause)"
    parts = []
    for lit in clause:
        parts.append(term_to_string(lit))
    return "  V  ".join(parts)


# 'Human' <-> '~Human'
def negate_name(name):
    if name.startswith('~'):
        return name[1:]
    return '~' + name


# Try to resolve two clauses. Returns a list of (resolvent, unifier) pairs.
def resolve(c1, c2):
    results = []
    for i in range(len(c1)):
        for j in range(len(c2)):
            l1 = c1[i]
            l2 = c2[j]
            if l1[0] == negate_name(l2[0]):          # complementary literals?
                a1 = [l1[0].lstrip('~')] + l1[1:]    # strip '~' to compare the atoms
                a2 = [l2[0].lstrip('~')] + l2[1:]
                theta = unify(a1, a2, {})            # <-- unification is used here
                if theta is not None:
                    new_clause = []
                    for k in range(len(c1)):         # everything except l1 ...
                        if k != i:
                            new_clause.append(apply_subst(c1[k], theta))
                    for k in range(len(c2)):         # ... and everything except l2
                        if k != j:
                            new_clause.append(apply_subst(c2[k], theta))
                    results.append((new_clause, theta))
    return results


# Keep resolving pairs of clauses until we get [] or run out of new clauses
def prove(clauses, max_rounds=10):
    known = []            # all clauses so far
    seen = []             # text of every clause, to avoid duplicates
    done = []             # pairs (i, j) already resolved
    for c in clauses:
        known.append(c)
        seen.append(clause_to_string(c))

    counter = 0
    for round_no in range(max_rounds):
        new_found = []
        for i in range(len(known)):
            for j in range(i + 1, len(known)):
                if (i, j) in done:
                    continue
                done.append((i, j))
                counter = counter + 1
                # rename variables so the two clauses never share a variable name
                c1 = rename(known[i], "_a" + str(counter))
                c2 = rename(known[j], "_b" + str(counter))
                for (res, theta) in resolve(c1, c2):
                    text = clause_to_string(res)
                    print("Resolve [%d] and [%d]  using %s" % (i + 1, j + 1, show_subst(theta)))
                    if len(res) == 0:
                        print("   -> " + text)
                        print("\nEmpty clause reached: the goal is PROVED.")
                        return True
                    if text not in seen:
                        seen.append(text)
                        new_found.append(res)
                        number = len(known) + len(new_found)
                        print("   -> [%d] %s" % (number, text))
                    else:
                        print("   -> (already known)")
        if len(new_found) == 0:
            print("\nNo new clauses: the goal cannot be proved.")
            return False
        for c in new_found:
            known.append(c)
    print("\nStopped (round limit).")
    return False


# ==================== MAIN ====================
print("===== PART 1: UNIFICATION =====\n")
tests = [
    (['Loves', 'John', '?x'],      ['Loves', '?y', 'Mary']),
    (['Knows', 'John', '?x'],      ['Knows', '?y', ['Mother', '?y']]),
    (['Likes', 'John', 'Apple'],   ['Likes', 'John', 'Banana']),
    (['P', '?x'],                  ['P', ['f', '?x']]),
    (['Eats', '?x', '?y'],         ['Eats', 'Ram', '?x']),
]
for a, b in tests:
    print(term_to_string(a), " <-> ", term_to_string(b))
    print("   Unifier:", show_subst(unify(a, b, {})), "\n")

print("===== PART 2: RESOLUTION (uses unification) =====\n")
kb = [
    [['~Human', '?x'], ['Mortal', '?x']],     # ~Human(x) V Mortal(x)
    [['Human', 'Socrates']],                  # Human(Socrates)
    [['~Mortal', 'Socrates']],                # negated goal
]
for i in range(len(kb)):
    print("[%d] %s" % (i + 1, clause_to_string(kb[i])))
print()
prove(kb)