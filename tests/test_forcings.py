import pandas as pd
import pytest
from case_base import CaseBase


@pytest.fixture
def simple_csv(tmp_path_factory):
    data = {
        "Col1": [1, 1, 1, 0],
        "Label": [1, 1, 0, 0],
    }
    df = pd.DataFrame(data)
    path = tmp_path_factory.mktemp("data") / "simple.csv"
    df.to_csv(path, index=False, header=True)
    return path


def test_number_of_inconsistent_forcing_relations_naive(simple_csv):
    CB = CaseBase(simple_csv)
    inds = range(len(CB))
    forcings = CB.get_forcings(inds)
    assert len(forcings) == 11
    cons_forcings = CB.remove_inconsistent_forcings(inds, forcings)
    assert len(cons_forcings) == 4
    assert len(forcings) - len(cons_forcings) == 7


def test_number_of_inconsistent_forcing_relations_relative(simple_csv):
    CB = CaseBase(simple_csv, auth_method="relative")
    inds = range(len(CB))
    forcings = CB.get_forcings(inds)
    assert len(forcings) == 9
    cons_forcings = CB.remove_inconsistent_forcings(inds, forcings)
    assert len(cons_forcings) == 4
    assert len(forcings) - len(cons_forcings) == 5


# def test_number_of_trivial_forcing_relations_naive():
#     assert False


# def test_number_of_trivial_forcing_relations_relative():
#     assert False
