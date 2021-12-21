# codesim

A similarity measurer on two programming assignments on Online Judge.

- Algorithm implementation details is at [here](http://www.stardustdl.top/posts/projects/codesim/).

## Install

Recommend OS: Ubuntu 20.04.

> Other Linux distribution is OK, but Windows and Mac OS with Python 3.10 may fail since codesim depends on [ortools](https://pypi.org/project/ortools/).

Install Python(>=3.7), pip, g++, and objdump.

An example script for Ubuntu 20.04.

```sh
# Ubuntu 20.04 has Python 3.8 installed, use python3 to run python
apt update
# Install g++ and objdump
apt install build-essential
```

**Development Way** Install requirements.

```sh
cd src
pip install -r requirements.txt
```

**Package Way** Build and install a portable Python Wheel package.

```sh
cp README.md ./src
cd src
python -m pip install --upgrade build twine
python -m build -o ../dist
python -m pip install ../dist/codesim-0.0.1-py3-none-any.whl
```

## Usage

**Development Way**

```sh
cd src
python -m codesim <file1> <file2>

# verbose mode to see log
python -m codesim <file1> <file2> [-v/-vv/-vvv..]
```

**Package Way** If you have installed the built package, then just use the installed package.

```sh
python -m codesim <file1> <file2>

codesim <file1> <file2>
```

## Reference

The code similarity measuring algorithm originates from

> Jiang Y, Xu C. Needle: Detecting code plagiarism on student submissions[C]//Proceedings of ACM Turing Celebration Conference-China. 2018: 27-32.
