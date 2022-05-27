import numpy as np
import pandas as pd
from tqdm import tqdm


# Recursive definition of the transitive closure.
def Rplus(x, R):
    return R[x] | {z for y in R[x] for z in Rplus(y, R)}


# Takes as input a (finite) Hasse Diagram, where the nodes are given by A and
# the covering relation by R, and return the reflexive transitive closure of R.
def tr_closure(A, R):
    R = {x: {y for y in A if (x, y) in R} for x in A}
    return {(x, x) for x in A} | {(x, y) for x in A for y in Rplus(x, R)}


def analyze(CB):
    print("\nComputing relevant differences between the cases.")
    inds = range(len(CB))

    # Now compute all forcing relations between the cases.
    F = {(i, j) for i in tqdm(inds) for j in inds if CB[i] <= CB[j]}
    Fd = {i: [] for i in inds}
    Fid = {i: [] for i in inds}
    for i, j in F:
        Fd[i] += [j]
        Fid[j] += [i]

    # Separate from F the forcings that lead to inconsistency.
    I = {(i, j) for (i, j) in F if CB[i].s != CB[j].s}
    Id = {i: set() for i in inds}
    for i, j in I:
        Id[i] |= {j}
        Id[j] |= {i}

    # Gather all landmarks for both classes.
    ls = {
        s: [
            i
            for i in inds
            if CB[i].s == s and not any(CB[i].s == CB[j].s for j in Fid[i] if i != j)
        ]
        for s in [0, 1]
    }

    # Make a DataFrame for holding the analysis results.
    adf = pd.DataFrame()
    adf["Scores"] = [len(Fd[i]) for i in inds]
    adf["Score (same outcome)"] = [len(Fd[i]) - len(Id[i]) for i in inds]
    adf["Score (diff outcome)"] = [len(Id[i]) for i in inds]
    adf["Consistency"] = [int(len(Id[i]) == 0) for i in inds]
    adf["Label"] = [CB[i].s for i in inds]
    adf["Landmark"] = [i in ls[CB[i].s] for i in inds]

    # Compute the minimum (?) number of deletions before the CB is consistent.
    removals = 0
    while sum(s := [len(Id[i]) for i in inds]) != 0:
        k = np.argmax(s)
        for i in inds:
            Id[i] -= {k}
        Id[k] = set()
        removals += 1

    # Print the results of the analysis.
    print(f"\nNumber of cases: {len(CB)}.")
    print(
        f"Percentage consistent cases: {round(adf['Consistency'].describe()['mean']*100, 1)}%."
    )
    print(f"Removals to obtain consistency: {round(removals/len(CB)*100, 1)}%.")
    print(
        f"Percentage trivial cases: {round(((len(CB) - (len(ls[0]) + len(ls[1]))) / len(CB)) * 100, 1)}%."
    )
    print(f"Number of landmarks: {len(ls[0]) + len(ls[1])}.")
