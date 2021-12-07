# codesim

## Install

1. Install Python(>=3.7) and pip
2. Install requirements.

```sh
cd src
pip install -r requirements.txt
```

## Usage

```sh
cd src
python -m codesim <file1> <file2>
```

## Alternative

Build and install a portable Python Wheel package.

```sh
cp README.md ./src
cd src
python -m pip install --upgrade build twine
python -m build -o ../dist
python -m pip install ../dist/codesim-0.0.1-py3-none-any.whl

codesim <file1> <file2>
```