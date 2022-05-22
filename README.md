![codesim](https://socialify.git.ci/StardustDL/codesim/image?description=1&font=Bitter&forks=1&issues=1&language=1&owner=1&pulls=1&stargazers=1&theme=Light)

![CI](https://github.com/StardustDL/codesim/workflows/CI/badge.svg) ![](https://img.shields.io/github/license/StardustDL/codesim.svg)

A similarity measurer on two programming assignments on Online Judge.

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

Some test cases are from [CodeNet Dataset](https://github.com/IBM/Project_CodeNet).

The code similarity measuring algorithm originates from

> Jiang Y, Xu C. Needle: Detecting code plagiarism on student submissions[C]//Proceedings of ACM Turing Celebration Conference-China. 2018: 27-32.

## Algorithm

> Algorithm implementation details are from [here](http://www.stardustdl.top/posts/projects/codesim/).

### Goals

We want to measure similarity between two programming assignments $A$ and $B$ on Online Judge to find possible plagiarism.
We assume that each input program is a single-file C++ program that can be compiled by `g++ -std=c++17 -pedantic`.

### Preprocessing

The compiling and optimization removes comments, macros and unnessesary code, ignores local variable names and code format.
Many redundant changes will have zero or minor impacts after compiler optimization and it is a good way to normalize a program.
To decrease obfuscation changes' impacts further, we use opcode sequence as a function's figureprint and ignore operands.

A program is a set of functions, and a function is a sequence of opcodes.

We first compile the input code by `g++` with `-O2` optimization level.
To keep the generated object file clean, we use `-c` option to prevent generating initializing function.

Then we use `objdump` to disassembly object files, collect and filter (ignore `nop` and unrecogized opcodes) opcode sequence.

### Similarity

One common kind of obfuscation changes is splitting one function into many functions.
To address this, we calculate inter-function similarity (as same as the program similarity) with intra-function similarity.
The main idea is mapping each instruction in program $A$ to the most similar instruction in program $B$.

#### Intra-function Similarity

Intra-function similarity models the similarity of a instruction in a specific function context.

Let $f\in A$ be a function from program $A$, and $g$ be a function from program $B$.
If $f$ can be extended to $g$, then there may be a code copy case.
We use longest common subsequence (LCS) to calculate the cost to extend $f$ to $g$.
To preserve integrity of $f$ during extending, we calculate the longest LCS in a fixed window size $\omega=\frac{3}{2}|f|$.

$$\sigma(f,g)=\max_{k\in\\{1,2,\dots,|g|\\}}\text{LCS}(f,g[k:k+\omega])$$

Formally, the intra-function similarity between $f$ and $g$ is defined as

$$\rho(f,g)=\frac{\max\\{\sigma(f_i,g_j),\sigma(g_j,f_i)\\}}{\min\\{|f_i|,|g_j|\\}}$$

For efficiency, we use the following strategies: use integer for opcode to speed up comparison, calculate $\sigma(f,g)$ by the following formula.

$$\sigma(f,g)=\begin{cases}
    \text{LCS}(f,g) & \omega>=|g| \\
    \max_{k\in\\{1,2,\dots,|g|-\omega\\}}\text{LCS}(f,g[k:k+\omega]) & \text{otherwise}
\end{cases}$$

#### Inter-function Similarity

We models the mapping problem by a weighted flow network graph $G=(V,E,c:E\rightarrow \mathbb{N},w:E\rightarrow \mathbb{R})$.

Let $n=|A|,m=|B|,i\in[n], j\in [m],f_i\in A,g_j\in B$.

$$\begin{aligned}
    V&=\\{s,t\\}\cup\\{l_i\\}\cup\\{r_j\\}\\
    E&=\\{(s,l_i)\\}\cup\\{(r_j,t)\\}\cup \\{(l_i,r_j)\\}\\
    c(s,l_i)&=|f_i|,w(s,l_i)=0\\
    c(r_j,t)&=|g_j|,w(r_j,t)=0\\
    c(l_i,r_j)&=\sigma(f_i,g_j)\\
    w(l_i,r_j)&=\text{sigmoid}'(\rho(f,g))
\end{aligned}$$

We use sigmoid function's center part, $\text{sigmoid}'(x)=\text{sigmoid}(\alpha x+\beta)$, with constants $\alpha=2,\beta=-1/2$ to normalize $\rho(f,g)$.

Then the unnormalized inter-function similarity from $A$ to $B$ is defined as

$$
\rho'(A\rightarrow B)=\frac{\text{MaximumWeightFlow(G)}}{\sum_{i}|f_i|}
$$

Then normalize $\rho'(A\rightarrow B)$ onto $[0,1]$.

$$
\rho(A\rightarrow B)=\frac{\rho'(A\rightarrow B)}{\text{sigmoid}'(1)}
$$

Finally the inter-function similarity between $A$ and $B$ is defined as the average of the two directions.

$$
\rho(A,B)=\frac{\rho(A\rightarrow B)+\rho(B\rightarrow A)}{2}
$$

For efficiency, we use the following strategies: calculate $\sigma(f_i,g_j)$ for all $(i,j)$ pairs parallel and cache the results, use integer $\lfloor \theta \cdot w(l_i,r_j) \rfloor$, in which $\theta=10000$, to replace the real number $w(l_i,r_j)$.
