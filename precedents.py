import numpy as np
from tqdm import tqdm


def determine_distribution(n_precedents):
    n_precedents = np.array(n_precedents)
    mean = n_precedents.mean()
    std = n_precedents.std()
    return mean, std


def get_precedent_distribution(CB):
    n_precedents = []
    for case in tqdm(CB):
        best_precedents = get_best_precedents(case, CB)
        n_precedents.append(len(best_precedents))
    return determine_distribution(n_precedents)


def get_best_precedents(f, CB):
    comparisons = get_comparisons(f, CB)
    bested = set()
    for c in comparisons:
        if c[0] not in bested:
            if CB.auth_method is None:
                bested = inner_loop_naive(comparisons, c, bested)
            else:
                bested = inner_loop_alpha(comparisons, c, bested)
    return [c for c in comparisons if c[0] not in bested]


def get_comparisons(f, CB):
    if CB.auth_method is None:
        return [
            (c.name, set(c.diff(f.F))) for c in CB if c.s == f.s and c.name != f.name
        ]
    else:
        return [
            (c.name, set(c.diff(f.F)), c.alpha)
            for c in CB
            if c.s == f.s and c.name != f.name
        ]


def inner_loop_naive(comparisons, c, bested):
    for oc in comparisons:
        if c[1] > oc[1] and c[0] != oc[0]:
            bested.add(c[0])
    return bested


def inner_loop_alpha(comparisons, c, bested):
    for oc in comparisons:
        if c[1] > oc[1] and c[0] != oc[0] and c[2] <= oc[2]:
            bested.add(c[0])
    return bested
