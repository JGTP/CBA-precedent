from case_base import CaseBase
from precedents import get_precedent_distribution


def test_best_precedent_distribution_naive(csv_file):
    CB = CaseBase(csv_file)
    mean, std = get_precedent_distribution(CB, None)
    assert round(mean, 2) == 5.29
    assert round(std, 2) == 1.75


def test_best_precedent_distribution_rel(csv_file):
    CB = CaseBase(csv_file)
    mean, std = get_precedent_distribution(CB, "relative")
    assert round(mean, 2) == 3.71
    assert round(std, 2) == 1.91


def test_best_precedent_distribution_abs(csv_file):
    CB = CaseBase(csv_file)
    mean, std = get_precedent_distribution(CB, "absolute")
    assert round(mean, 2) == 3.71
    assert round(std, 2) == 1.58


def test_best_precedent_distribution_prod(csv_file):
    CB = CaseBase(csv_file)
    mean, std = get_precedent_distribution(CB, "product")
    assert round(mean, 2) == 3.71
    assert round(std, 2) == 1.58


def test_best_precedent_distribution_harm(csv_file):
    CB = CaseBase(csv_file)
    mean, std = get_precedent_distribution(CB, "harmonic")
    assert round(mean, 2) == 3.71
    assert round(std, 2) == 1.58
