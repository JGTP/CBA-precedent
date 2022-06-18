import pandas as pd
import pytest
from case_base import CaseBase


@pytest.fixture(scope="session")
def csv_file(tmp_path_factory):
    data = {
        "Gift": [0, 1, 1],
        "Present": [0, 0, 1],
        "Website": [0, 5, 15],
        "High-cost": [0, 1, 0],
        "Label": [1, 1, 0],
    }
    df = pd.DataFrame(data)
    path = tmp_path_factory.mktemp("test_data") / "test.csv"
    df.to_csv(path, index=False, header=True)
    return path


def test_absolute_authoritativeness(csv_file):
    CB = CaseBase(csv_file)
    precedents = absolute_auth_precedents(f, CB)
    assert len(precedents) == 2
    assert precedent[0] == []
    assert precedent[1] == []


def test_relative_authoritativeness():
    assert False


def test_product_authoritativeness():
    assert False


def test_harmonic_authoritativeness():
    assert False
