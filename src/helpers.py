# Recursive definition of the transitive closure.
import numpy as np
from tqdm import tqdm


def Rplus(x, R):
    return R[x] | {z for y in R[x] for z in Rplus(y, R)}


# Takes as input a (finite) Hasse Diagram, where the nodes are given by A and
# the covering relation by R, and return the reflexive transitive closure of R.
def tr_closure(A, R):
    R = {x: {y for y in A if (x, y) in R} for x in A}
    return {(x, x) for x in A} | {(x, y) for x in A for y in Rplus(x, R)}


def get_precedent_distribution(CB, auth_method=None):
    n_precedents = []
    for case in tqdm(CB, miniters=100):
        if auth_method is None:
            n_precedents.append(n_agreement(case, CB))
        elif auth_method == "relative":
            n_precedents.append(relative_auth_precedents(case, CB))
        elif auth_method == "absolute":
            n_precedents.append(absolute_auth_precedents(case, CB))
        elif auth_method == "product":
            n_precedents.append(product_auth_precedents(case, CB))
        elif auth_method == "harmonic":
            n_precedents.append(harmonic_auth_precedents(case, CB))
    return determine_distribution(n_precedents)


def n_agreement(case, CB):
    # given a case index and a case base, returns a list of best precedents as comparisons
    same_outcome = [c for c in CB if c.s == case.s]
    precedents = []
    for other_case in same_outcome:
        if case <= other_case:
            precedents.append(other_case.name)
    return len(precedents)


def n_disagreement(case, CB):
    same_outcome = [c for c in CB if c.s != case.s]
    precedents = []
    for other_case in same_outcome:
        if case <= other_case:
            precedents.append(other_case.name)
    return len(precedents)


def relative_auth_precedents(case, CB):
    n_a = n_agreement(case, CB)
    n_d = n_disagreement(case, CB)
    return n_a / (n_a + n_d)


def absolute_auth_precedents(case, CB):
    n_a = n_agreement(case, CB)
    return n_a / len(CB)


def product_auth_precedents(case, CB):
    rels = relative_auth_precedents(case, CB)
    abss = absolute_auth_precedents(case, CB)
    return rels * abss


def harmonic_auth_precedents(case, CB, beta=1):
    rels = relative_auth_precedents(case, CB)
    abss = absolute_auth_precedents(case, CB)
    return (1 + beta**2) * (rels * abss) / (rels + abss)


def determine_distribution(n_precedents):
    n_precedents = np.array(n_precedents)
    mean = n_precedents.mean()
    std = n_precedents.std()
    return mean, std
