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
        if CB.auth_method is None:
            best_precedents = get_best_precedents_naive(case, CB)
        else:
            best_precedents = get_best_precedents_alpha(case, CB)
        n_precedents.append(len(best_precedents))
    return determine_distribution(n_precedents)


def get_best_precedents_naive(f, CB):
    same_outcome = [c for c in CB if (c.s == f.s) and (c.name != f.name)]
    bested = set()
    for c in same_outcome:
        if c.name not in bested:
            bested = inner_loop_naive(f, same_outcome, c, bested)
    return [c for c in same_outcome if c.name not in bested]


def inner_loop_naive(f, same_outcome, c, bested):
    for oc in same_outcome:
        if set(c.diff(f.F)) > set(oc.diff(f.F)):
            bested.add(c.name)
    return bested


def get_best_precedents_alpha(f, CB):
    same_outcome = [c for c in CB if (c.s == f.s) and (c.name != f.name)]
    bested = set()
    for c in same_outcome:
        bested = inner_loop_alpha(f, same_outcome, c, bested)
    return [c for c in same_outcome if c.name not in bested]


def inner_loop_alpha(f, same_outcome, c, bested):
    for oc in same_outcome:
        if c.name not in bested:
            if any(c.diff(f.F)):
                if oc.name != c.name:
                    if c.alpha > oc.alpha:
                        bested.add(oc.name)
        else:
            break
    return bested
