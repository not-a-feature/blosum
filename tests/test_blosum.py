# Testing BLOSUM Handling
import blosum as bl
import pytest
from os import path


f = float("-inf")


@pytest.mark.parametrize(
    "blosum_number,expected",
    [
        (45, [0, 1, -2, -5, 3, 1, -3, -5, -2, -2, 1, -5, f, f, f, f]),
        (50, [0, 1, -1, -5, 3, 2, -4, -5, -3, -1, 1, -5, f, f, f, f]),
        (62, [0, 0, -1, -4, 2, 1, -3, -4, -3, -2, 1, -4, f, f, f, f]),
        (90, [0, 1, -2, -6, 2, 1, -4, -6, -4, -3, 0, -6, f, f, f, f]),
    ],
)
def test_blosum(blosum_number, expected):
    bm = bl.BLOSUM(blosum_number)

    get_test = []

    for a in ["H", "K", "W", "U"]:
        for b in ["R", "Q", "F", "*"]:
            get_test.append(bm[a][b])

    assert get_test == expected


def test_blosum_default():
    bm = bl.BLOSUM(62, default=-99)
    assert bm["non"]["existent"] == -99  # test default value
    assert dict(bm["nonexistent"]) == dict()  # test default value
    assert bm["H"]["F"] == -1  # test real value


@pytest.mark.filterwarnings("ignore:Blosum")
def test_blosum_custom_file():
    fp = path.join(path.dirname(__file__), "test.blosum")
    bm = bl.BLOSUM(fp)
    labels = ["A", "R", "N", "D"]
    s = sum([bm[a][b] for b in labels for a in labels])
    assert s == 19


@pytest.mark.filterwarnings("ignore:Blosum")
def test_blosum_custom_file_with_comments():
    fp = path.join(path.dirname(__file__), "comments.blosum")
    bm = bl.BLOSUM(fp)
    labels = ["A", "R", "N", "D"]
    s = sum([bm[a][b] for b in labels for a in labels])
    assert s == 17


@pytest.mark.xfail
def test_blosum_invalid_file():
    fp = path.join(path.dirname(__file__), "fail.blosum")
    bm = bl.BLOSUM(fp)
    bm["A"]["B"]


@pytest.mark.xfail
def test_blosum_invalid_file2():
    fp = path.join(path.dirname(__file__), "fail2.blosum")
    bm = bl.BLOSUM(fp)
    bm["A"]["B"]


@pytest.mark.xfail
def test_blosum_empty():
    bm = bl.BLOSUM(None)
    bm["A"]["B"]


def test_magic_repr():
    assert repr(bl.BLOSUM(62)) == "BLOSUM(62, default=float('-inf'))"
    assert repr(bl.BLOSUM(62, default=float("inf"))) == "BLOSUM(62, default=float('inf'))"
    assert repr(bl.BLOSUM(62, default=0)) == "BLOSUM(62, default=0)"

    fp = path.join(path.dirname(__file__), "test.blosum")
    assert repr(bl.BLOSUM(fp, default=0)) == f'BLOSUM("{fp}", default=0)'
