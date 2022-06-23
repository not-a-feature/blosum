![blosum](https://github.com/not-a-feature/blosum/raw/main/blosum.png)

A small module for easy access to BLOSUM matrices without dependencies.

![Test Badge](https://github.com/not-a-feature/blosum/actions/workflows/tests.yml/badge.svg)
![Python Version Badge](https://img.shields.io/pypi/pyversions/blosum)
![Download Badge](https://img.shields.io/pypi/dm/blosum.svg)
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/blosum/README.html)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The BLOcks SUbstitution Matrices (BLOSUM) are used to score alignments between protein sequences and are therefore mainly used in bioinformatics.

Reading such matrices is not particularly difficult, yet most off the shelf packages are overloaded with strange dependencies.
And why do we need to implement the same reader again if there is a simple module for that.

`blosum` offers a robust and easy-to-expand implementation without relying on third-party libraries. 


## Installation
Using pip  / pip3:
```bash
pip install blosum
```
Or by source:
```bash
git clone git@github.com:not-a-feature/blosum.git
cd blosum
pip install .
```

Or by conda:
```bash
conda install blosum
```
## How to use

### Default BLOSUM 
This package provides the most commonly used BLOSUM matrices.
You can choose from BLOSUM 45, 50, 62, 80 and 90.

To load a matrix:
```python
import blosum as bl
matrix = bl.BLOSUM(62)
``` 

### Custom Matrix
In addition, own matrices can be loaded. For this, the path is given as an argument.

```python
import blosum as bl
matrix = bl.BLOSUM("path/to/blosum.file")
```

The matrices are required to have following format:

```
# Comments should start with #
# Each value should be seperated by one or many whitespace
   A  R  N  D
A  5 -2 -1 -2
R -2  7  0 -1
N -1  0  6  2
D -2 -1  2  7
```

### Getting Values.
To get a value use:

```python
val = matrix["AY"]
```

Or get the dictionary representation of the BLOSUM matrix.

```python
blosum_dict = dict(matrix)
```

If the key cannot be found, the default value is returned. It is `float("-inf")`.
It is possible to set a custom default score:
```python
matrix = bl.BLOSUM(62, default=0)
```

## License
```
Copyright (C) 2022 by Jules Kreuer - @not_a_feature
This piece of software is published unter the GNU General Public License v3.0
TLDR:

| Permissions      | Conditions                   | Limitations |
| ---------------- | ---------------------------- | ----------- |
| ✓ Commercial use | Disclose source              | ✕ Liability |
| ✓ Distribution   | License and copyright notice | ✕ Warranty  |
| ✓ Modification   | Same license                 |             |
| ✓ Patent use     | State changes                |             |
| ✓ Private use    |                              |             |
```
Go to [LICENSE.md](https://github.com/not-a-feature/blosum/blob/main/LICENSE) to see the full version.

## Dependencies
In addition to packages included in Python 3, this piece of software uses 3rd-party software packages for development purposes that are not required in the published version.
Go to [DEPENDENCIES.md](https://github.com/not-a-feature/blosum/blob/main/DEPENDENCIES.md) to see all dependencies and licenses.
