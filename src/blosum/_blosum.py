"""
blosum: A simple BLOSUM toolbox
See: https://github.com/not-a-feature/blosum
Or:  https://pypi.org/project/blosum/

@author: Jules Kreuer / not_a_feature
License: GPL-3.0
"""

from warnings import warn
from ._data import default_blosum
from collections import defaultdict
from typing import Dict, Union, DefaultDict


class BLOSUM(defaultdict):  # type: ignore
    def __init__(self, n: Union[int, str], default: float = float("-inf")):
        """
        Object to easily access a blosum matrix.
        This reader supports asymetric data.

        Input
        -----
            Either n ϵ {45,50,62,80,90} or path

            n: int, which BLOSUM Matrix to use.
                Choice between: 45,50,62,80 and 90
                Data gathered from https://www.ncbi.nlm.nih.gov/IEB/ToolBox/C_DOC/lxr/source/data/

            path: string, path to a Blosum matrix.
                File in a format like:
                https://www.ncbi.nlm.nih.gov/IEB/ToolBox/C_DOC/lxr/source/data/BLOSUM62

            default: float, default -inf
        """

        self.n = n
        self.default = default

        # Using default matrix
        if isinstance(n, int) and n in [45, 50, 62, 80, 90]:
            matrix = {}
            for k, v in default_blosum[n].items():
                matrix[k] = defaultdict(lambda: default, v)
            super().__init__(lambda: defaultdict(lambda: default), matrix)

        # load custom matrix
        elif isinstance(n, str):
            super().__init__(lambda: defaultdict(lambda: default), loadMatrix(n))
        else:
            raise (
                BaseException(
                    f"""Unknown BLOSUM Number '{n}'. Choose n ϵ {{45,50,62,80,90}} or provide a path to a matrix."""
                )
            )

    def __str__(self) -> str:
        """
        Magic method to allow BLOSUM object printing.
        """
        return f"BLOSUM({self.n}, default={self.default}, {dict(self)}"

    def __repr__(self) -> str:
        """
        Magic method to allow printing of the BLOSUM representation.
        """
        if self.default == float("-inf"):
            d = "float('-inf')"
        elif self.default == float("inf"):
            d = "float('inf')"
        else:
            d = str(self.default)

        if self.n in [45, 50, 62, 80, 90]:
            n = self.n
        else:
            n = f'"{self.n}"'

        return f"BLOSUM({n}, default={d})"


def loadMatrix(
    path: str,
    default: float = float("-inf"),
) -> DefaultDict[str, DefaultDict[str, float]]:
    """
    Reads a Blosum matrix from file.
    File in a format like:
        https://www.ncbi.nlm.nih.gov/IEB/ToolBox/C_DOC/lxr/source/data/BLOSUM62

    Input
    -----
        path: str, path to a file.
        default: float, default value "-inf"

    Returns
    -------
        blosumDict: Dictionary, The blosum dict
    """

    with open(path, "r") as f:
        content = f.readlines()

    blosumDict: DefaultDict[str, DefaultDict[str, float]] = defaultdict(
        lambda: defaultdict(lambda: default)
    )

    header = True
    for line in content:
        line = line.strip()

        # Skip comments starting with #
        if line.startswith("#"):
            continue

        linelist = line.split()

        # Extract labels only once
        if header:
            labelslist = linelist
            header = False

            # Check if all AA are covered
            if not len(labelslist) == 25:
                warn(UserWarning("Blosum matrix may not cover all amino-acids"))
            continue

        if not len(linelist) == len(labelslist) + 1:
            # Check if line has as may entries as labels
            raise EOFError("Blosum file is missing values.")

        # Add Line/Label combination to dict
        for index, lab in enumerate(labelslist, start=1):
            blosumDict[linelist[0]][lab] = float(linelist[index])

    # Check quadratic
    if not len(blosumDict) == len(labelslist):
        raise EOFError("Blosum file is not quadratic.")

    return blosumDict
