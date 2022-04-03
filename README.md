# nyu-ai-lab-3

NYU Artificial Intelligence Course Lab 3: A generic Markov process solver.

## Prerequisite

-   Python 3.8+

## Getting-started

### Switch to Python 3.8 on CIMS machines

The Python version has to at least have full type hint support, thus requiring Python 3.8+.

```bash
module load python-3.8
```

If successful, the command `python3 --version` should give you:

```bash
$ python3 --version
Python 3.8.6
```

### Script usages

> The main entrance is a python script, not a binary. It is in Shebang style,
> thus can be executed directly.

Use `./mdp -h` command to see the usage:

```
usage: mdp [-h] [-d DISCOUNT] [-m] [-t TOLERANCE] [-i ITERATION] inputfile

A generic Markov process solver.

positional arguments:
  inputfile             input file path

optional arguments:
  -h, --help            show this help message and exit
  -d DISCOUNT, --discount DISCOUNT
                        a float discount factor [0, 1] to use on future rewards, defaults to 1.0 if not set
  -m, --min             whether to minimize values as costs, defaults to false which maximizes values as rewards
  -t TOLERANCE, --tolerance TOLERANCE
                        a float tolerance for convergence, defaults to 0.01 if not set
  -i ITERATION, --iteration ITERATION
                        the maximum number of iterations to run, defaults to 100 if not set
```

Examples:

```bash
$ ./mdp input.txt
```

```bash
$ ./mdp -t 0.001 -i 1000 input.txt
```

```bash
$ ./mdp --discount 0.9 --min input.txt
```

## Project structure

```
project
├─solving                       solving python module
│  ├─__init__.py                    Module initialization
│  ├─node.py                            Markov Node class
│  ├─parser.py                          A parser for the input file
│  └─solver.py                          MDP solver that takes the parsed as input
│
├─mdp                           Main entrance python script (shebang style)
└─README.md                     The file you're reading
```
