# Testing BLOSUM Handling
import blosum as bl
import pytest
from os import path


f = float("-inf")


@pytest.mark.filterwarnings("ignore:Blosum")
def test_loadMatrix_eq_blosum():
    fp = path.join(path.dirname(__file__), "test.blosum")
    bm = dict(bl.BLOSUM(fp))

    assert bm == bl.loadMatrix(fp)
