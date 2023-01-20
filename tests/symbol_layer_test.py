import math
import string

from xsystem import build_new_symbol
from xsystem import AsciiClass
from xsystem import merge_symbols
from xsystem import Symbol


def test_get_ascii_class():
    for c in string.printable:
        ascii_class = AsciiClass.get_ascii_class(c)

        assert ascii_class is not None
        assert ascii_class in AsciiClass


def test_symbol_creation():
    symbol = build_new_symbol("5")

    assert symbol

    assert 0 == symbol.fit_score("5", math.inf)


def test_symbols_character_letters():
    for l in string.ascii_letters:
        l_class = AsciiClass.get_ascii_class(l)

        assert l_class in {
            AsciiClass.UPPER, AsciiClass.LOWER, AsciiClass.ALPHA
        }

        assert l in AsciiClass.get_class_characters(l_class)


def test_symbols_charater_digits():
    for d in string.digits:
        d_class = AsciiClass.get_ascii_class(d)

        assert d_class in {
            AsciiClass.DIGIT
        }

        assert d in AsciiClass.get_class_characters(d_class)


def test_symbol_merge_same_class():
    symbol = Symbol(
        chars={"a"},
        s_class=AsciiClass.LOWER,
        is_class=False
    )

    merged = merge_symbols("b", symbol)

    assert merged is not None
    assert not merged.is_class
    assert len(merged.chars) == 2
    assert merged.s_class == AsciiClass.LOWER


def test_symbol_merge_different_class():
    symbol = Symbol(
        chars={"a"},
        s_class=AsciiClass.LOWER,
        is_class=False
    )

    merged = merge_symbols("1", symbol)

    assert merged is not None
    assert not merged.is_class
    assert len(merged.chars) == 2
    assert merged.s_class == AsciiClass.ALNUM


def test_symbol_merge_to_class():
    symbol = Symbol(
        chars=set([s for s in AsciiClass.get_class_characters(AsciiClass.LOWER) if s != "c"]),
        s_class=AsciiClass.LOWER,
        is_class=False
    )

    assert len(symbol.chars) == len(AsciiClass.get_class_characters(AsciiClass.LOWER)) - 1

    merged = merge_symbols("c", symbol)

    assert merged.is_class
    assert len(merged.chars) == len(AsciiClass.get_class_characters(AsciiClass.LOWER))
    assert merged.s_class == AsciiClass.LOWER
