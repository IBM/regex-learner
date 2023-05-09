# Regex-learner

This project provides a tool/library implementing an automated regular expression building mechanism.

This project takes inspiration on the paper from Ilyas, et al [1]

[Ilyas, Andrew, M. F. da Trindade, Joana, Castro Fernandez, Raul and Madden, Samuel. 2018. "Extracting Syntactical Patterns from Databases."](https://hdl.handle.net/1721.1/137774)

This repository contains code and examples to assist in the exeuction of regular expression learning from the columns of data.

This is a basic readme. It will be completed as the prototype grows.

# Installation

The project can be installed via pip:
```bash
pip install xsystem
```

# Examples of usage

Example of learning a date pattern from 100 examples of randomly sampled dates in the format DD-MM-YYYY.

```python
from xsystem import XTructure
from faker import Faker

fake = Faker()
x = XTructure() # Create basic XTructure class

for _ in range(100):
    d = fake.date(pattern=r"%d-%m-%Y") # Create example of data - date in the format DD-MM-YYYY
    x.learn_new_word(d) # Add example to XSystem and learn new features

print(str(x)) # ([0312][0-9])(-)([01][891652073])(-)([21][09][078912][0-9])
```

Similary, the tool can be used directly from the command line using the `regex-learner` CLI provided by the installation of the package.

The tool has several options, as described by the help message:

```
> regex-learner -h
usage: regex-learner [-h] [-i INPUT] [-o OUTPUT] [--max-branch MAX_BRANCH] [--alpha ALPHA] [--branch-threshold BRANCH_THRESHOLD]

A simple tool to learn human readable a regular expression from examples

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to the input source, defaults to stdin
  -o OUTPUT, --output OUTPUT
                        Path to the output file, defaults to stdout
  --max-branch MAX_BRANCH
                        Maximum number of branches allowed, defaults to 8
  --alpha ALPHA         Weight for fitting tuples, defaults to 1/5
  --branch-threshold BRANCH_THRESHOLD
                        Branching threshold, defaults to 0.85, relative to the fitting score alpha
```

Assuming a data file containing the examples to learn from is called `EXAMPLE_FILE`, and assuming one is interested in a very simple regular expression, the tool can be used as follows:

```bash
cat EXAMPLE_FILE | regex-learner --max-branch 2
```

## Note
Note that this project is not based on the actual implementation of the paper as presented in [2]

## References
1. Ilyas, Andrew, et al. "Extracting syntactical patterns from databases." 2018 IEEE 34th International Conference on Data Engineering (ICDE). IEEE, 2018.
2. https://github.com/mitdbg/XSystem
