import pandas as pd
import pytest
from case_base import CaseBase


@pytest.fixture
def simple_csv(tmp_path_factory):
    data = {
        "Col1": [1, 1, 1],
        "Label": [1, 1, 0],
    }
    df = pd.DataFrame(data)
    path = tmp_path_factory.mktemp("data") / "simple.csv"
    df.to_csv(path, index=False, header=True)
    return path


def test_number_of_forcing_relations_naive(simple_csv):
    CB = CaseBase(simple_csv)
    forcings = CB.get_forcings(range(len(CB)))
    assert len(forcings) == 3


def test_number_of_forcing_relations_relative():
    assert False


def test_number_of_inconsistent_forcing_relations_naive():
    assert False


def test_number_of_inconsistent_forcing_relations_relative():
    assert False


def test_number_of_trivial_forcing_relations_naive():
    assert False


def test_number_of_trivial_forcing_relations_relative():
    assert False
