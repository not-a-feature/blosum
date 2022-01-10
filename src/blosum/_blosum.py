"""
blosum: A simple BLOSUM toolbox
See: https://github.com/not-a-feature/blosum
Or:  https://pypi.org/project/blosum/

@author: Jules Kreuer / not_a_feature
License: GPL-3.0
"""

from warnings import warn
from ._data import default_blosum

class BLOSUM():
    def __init__(self, n, default: float = float("-inf")):
        """
        Object to easily access a blosum matrix.
        This reader supports asymetric data.

        Input:
        Either n ϵ {45,50,62,80,90} or path

        n: Int, which BLOSUM Matrix to use.
            Choice between: 45,50,62,80 and 90
            Data gathered from https://www.ncbi.nlm.nih.gov/IEB/ToolBox/C_DOC/lxr/source/data/

        path: String, path to a Blosum matrix.
            File in a format like:
            https://www.ncbi.nlm.nih.gov/IEB/ToolBox/C_DOC/lxr/source/data/BLOSUM62

        """

        self.n = n
        self.default = default

        # Using default matrix
        if n in [45, 50, 62, 80, 90]:
            self.matrix = default_blosum[n]

        elif isinstance(n, str):
            # load custom matrix
            self.__loadMatrix(n)
        else:
            raise(BaseException("Can't initate empty BLOSUM Object"))

    def __loadMatrix(self, path: str) -> None:
        """
        Reads a Blosum matrix from file.
        File in a format like:
            https://www.ncbi.nlm.nih.gov/IEB/ToolBox/C_DOC/lxr/source/data/BLOSUM62

        Input:
            path: str, path to a file.

        Returns:
            blosumDict: Dictionary, Blosum-Dict
        """

        with open(path, "r") as f:
            content = f.readlines()

        # Skip header line
        content = content[1:]

        # Extract labels
        labels = content[0]
        labelslist = labels.split()

        # Check if quadratic
        if not len(labelslist) == len(content)-1:
            raise EOFError("Blosum file is not quadratic.")

        # Check if all AA are covered
        if not len(labelslist) == 25:
            warn(UserWarning("Blosum matrix may not cover all amino-acids"))

        # Skip label line
        content = content[1:]

        blosumDict = {}
        # For each line
        for line in content:
            linelist = line.split()
            if len(linelist) < 0:
                break
            # Add Line/Label combination to dict
            for index, lab in enumerate(labelslist, start=1):
                blosumDict[f"{linelist[0]}{lab}"] = float(linelist[index])

        self.matrix = blosumDict

    def keys(self):
        """
        Returns the keys of the blosum matrix
        """
        return self.matrix.keys()

    def __getitem__(self, key: str) -> float:
        """
        Magic method to get the BLOSUM score.

        Input:
            key: String, Combination of both amino-acids.
        Ouput:
            score: Float, value or default value.isinstance(self.n, )
        """

        try:
            score = self.matrix[key]
        except KeyError:
            score = self.default

        return score

    def __str__(self) -> str:
        """
        Magic method to allow BLOSUM object printing.
        """
        return f'BLOSUM {self.n}\n{self.matrix}'

    def __repr__(self) -> str:
        """
        Magic method to allow printing of the BLOSUM representation.
        """

        d = "float('-inf')" if self.default == float("-inf") else self.default
        if self.n in [45, 50, 62, 80, 90]:
            n = self.n
        else:
            n = f'"{self.n}"'
        return f'BLOSUM({n}, default={d})'
