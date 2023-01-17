import string

from xsystem import get_ascii_class
from xsystem import AsciiClass


def test_get_ascii_class():
    for c in string.printable:
        # print(f"{c} is {get_ascii_class(c)}")
        ascii_class = get_ascii_class(c)

        assert ascii_class is not None
        assert ascii_class in AsciiClass



