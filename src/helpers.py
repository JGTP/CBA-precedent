from multiprocessing.sharedctypes import Value
import numpy as np
from tqdm import tqdm

from case import Case


def get_n_removals(inds, Id):
    # Compute the minimum (?) number of deletions before the CB is consistent.
    removals = 0
    while sum(s := [len(Id[i]) for i in inds]) != 0:
        k = np.argmax(s)
        for i in inds:
            Id[i] -= {k}
        Id[k] = set()
        removals += 1
    return removals


def get_landmarks(CB, inds, Fid):
    # Gather all landmarks for both classes.
    ls = {
        outcome: [
            i
            for i in inds
            if CB[i].outcome == outcome and not any(CB[i].outcome == CB[j].outcome for j in Fid[i] if i != j)
        ]
        for outcome in [0, 1]
    }
    return ls


def get_forcing_relations(CB, inds):
    # Now compute all forcing relations between the cases.
    fact_situation = {(i, j) for i in tqdm(inds) for j in inds if CB[i] <= CB[j]}
    Fd = {i: [] for i in inds}
    Fid = {i: [] for i in inds}
    for i, j in fact_situation:
        Fd[i] += [j]
        Fid[j] += [i]
    return fact_situation, Fd, Fid


def separate_inconsistent_forcings(CB, inds, fact_situation):
    # Separate from F the forcings that lead to inconsistency.
    I = {(i, j) for (i, j) in fact_situation if CB[i].outcome != CB[j].outcome}
    Id = {i: set() for i in inds}
    for i, j in I:
        Id[i] |= {j}
        Id[j] |= {i}
    return Id


def check_consistency(CB):
    # Given a CB, returns whether it is consistent + a sorted dictionary with the inconsistency of cases.
    other_cases = []
    consistent = True
    for case in CB.cases:
        for other_case in CB.cases:
            if case.outcome != other_case.outcome:
                if not other_case.diff(case):
                    consistent = False
                    other_cases.append(other_case.index)

    freq = {}
    for item in other_cases:
        if item in freq:
            freq[item] += 1
        else:
            freq[item] = 1
    sort_freq = {
        k: v for k, v in sorted(freq.items(), key=lambda item: item[1], reverse=True)
    }

    return consistent, sort_freq


def make_consistent(CB, n_removals):
    # Given a CB and the number of cases to remove per iteration, returns a consistent CB.

    consistent, case_dict = check_consistency()

    while not consistent:
        removals = []
        for r in list(case_dict.keys())[0:n_removals]:
            for case in CB.cases:
                if case.name == r:
                    removals.append(case)

        for r in removals:
            CB.cases.remove(r)

        consistent, case_dict = check_consistency()

    return CB
