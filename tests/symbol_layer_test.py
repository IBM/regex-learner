import string

from xsystem import get_ascii_class
from xsystem import build_new_symbol
from xsystem import get_class_characters
from xsystem import AsciiClass


def test_get_ascii_class():
    for c in string.printable:
        # print(f"{c} is {get_ascii_class(c)}")
        ascii_class = get_ascii_class(c)

        assert ascii_class is not None
        assert ascii_class in AsciiClass


def test_symbol_creation():
    symbol = build_new_symbol("5")

    assert symbol

    assert 0 == symbol.d("5")


def test_symbols_character_letters():
    for l in string.ascii_letters:
        l_class = get_ascii_class(l)

        assert l_class in {
            AsciiClass.UPPER, AsciiClass.LOWER, AsciiClass.ALPHA
        }

        assert l in get_class_characters(l_class)


def test_symbols_charater_digits():
    for d in string.digits:
        d_class = get_ascii_class(d)

        assert d_class in {
            AsciiClass.DIGIT
        }

        assert d in get_class_characters(d_class)
