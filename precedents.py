import numpy as np
from tqdm import tqdm

from authoritativeness import alpha, relative_authoritativeness


def get_precedent_distribution(CB, auth_method=None):
    n_precedents = []
    for case in tqdm(CB):
        best_precedents = get_best_precedents(case, CB, auth_method)
        n_precedents.append(len(best_precedents))
    return determine_distribution(n_precedents)


def determine_distribution(n_precedents):
    n_precedents = np.array(n_precedents)
    mean = n_precedents.mean()
    std = n_precedents.std()
    return mean, std


def get_best_precedents(case, CB, method):
    if method is None:
        same_outcome = [c for c in CB if c.s == case.s]
    else:
        same_outcome = [
            c
            for c in CB
            if (c.s == case.s and alpha(c, CB, method) >= alpha(case, CB, method))
        ]
    opposite_outcome = [c for c in CB if (c.s != case.s and c <= case)]
    return [c for c in same_outcome if c not in opposite_outcome]
