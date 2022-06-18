from case_base import CaseBase
from precedents import get_best_precedents


def test_find_best_precedents_naive(csv_file):
    CB = CaseBase(csv_file)
    case = CB[0]
    precedents = get_best_precedents(case, CB, None)
    assert len(precedents) == 6


def test_find_best_precedents_rel(csv_file):
    CB = CaseBase(csv_file)
    case = CB[0]
    precedents = get_best_precedents(case, CB, "relative")
    assert len(precedents) == 4


def test_find_best_precedents_abs(csv_file):
    CB = CaseBase(csv_file)
    case = CB[0]
    precedents = get_best_precedents(case, CB, "absolute")
    assert len(precedents) == 3


def test_find_best_precedents_prod(csv_file):
    CB = CaseBase(csv_file)
    case = CB[0]
    precedents = get_best_precedents(case, CB, "product")
    assert len(precedents) == 3


def test_find_best_precedents_harm(csv_file):
    CB = CaseBase(csv_file)
    case = CB[0]
    precedents = get_best_precedents(case, CB, "harmonic")
    assert len(precedents) == 3
