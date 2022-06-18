import pandas as pd
import pytest
from case_base import CaseBase
from helpers import (
    absolute_auth_precedents,
    harmonic_auth_precedents,
    product_auth_precedents,
    relative_auth_precedents,
)


@pytest.fixture(scope="session")
def csv_file(tmp_path_factory):
    data = {
        "Gift": [1, 1, 1, 1, 1, 1, 1],
        "Present": [1, 1, 1, 1, 1, 1, 1],
        "Website": [0, 0, 0, 2, 2, 2, 15],
        "High-cost": [0, 0, 0, 0, 0, 0, 0],
        "Label": [1, 1, 1, 1, 1, 0, 1],
    }
    df = pd.DataFrame(data)
    path = tmp_path_factory.mktemp("data") / "test.csv"
    df.to_csv(path, index=False, header=True)
    return path


def test_absolute_authoritativeness(csv_file):
    CB = CaseBase(csv_file)
    case = CB[0]
    auth = absolute_auth_precedents(case, CB)
    assert auth == 6 / 7


def test_relative_authoritativeness(csv_file):
    CB = CaseBase(csv_file)
    case = CB[5]
    auth = relative_auth_precedents(case, CB)
    assert auth == 1 / 6


def test_product_authoritativeness(csv_file):
    CB = CaseBase(csv_file)
    case = CB[0]
    auth = product_auth_precedents(case, CB)
    assert auth == (6 / 7) * (6 / 7)


def test_harmonic_authoritativeness(csv_file):
    CB = CaseBase(csv_file)
    case = CB[0]
    auth = harmonic_auth_precedents(case, CB)
    assert auth == 2 * ((6 / 7) * (6 / 7)) / ((6 / 7) + (6 / 7))
