# Regex-learner

This project implements and extends an automated regular expression building method firsty proposed in the following paper: 

[Ilyas, Andrew, M. F. da Trindade, Joana, Castro Fernandez, Raul and Madden, Samuel. 2018. "Extracting Syntactical Patterns from Databases."](https://hdl.handle.net/1721.1/137774)

This repository contains code and examples to assist in the exeuction of regular expression learning from the columns of data.

This is a basic readme. It will be completed as the prototype grows.

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
