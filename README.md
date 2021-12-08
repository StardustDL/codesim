# codesim

## Install

Install Python(>=3.7) and pip.

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
