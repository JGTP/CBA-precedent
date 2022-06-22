from case_base import CaseBase
from precedents import get_precedent_distribution


def test_best_precedent_distribution_naive(csv_file):
    CB = CaseBase(csv_file)
    mean, std = get_precedent_distribution(CB)
    assert round(mean, 2) == 2.71
    assert round(std, 2) == 1.58


def test_best_precedent_distribution_rel(csv_file):
    CB = CaseBase(csv_file, auth_method="relative")
    mean, std = get_precedent_distribution(CB)
    assert round(mean, 2) == 3.43
    assert round(std, 2) == 1.68
