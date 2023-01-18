from xsystem import BranchLayer
from xsystem import TokenLayer
from xsystem import SymbolLayer
from xsystem import AsciiClass
from xsystem import get_class_characters
import pytest


def test_add():
    # branch for "\d{4}"
    # examples: 1234

    branch = BranchLayer(
        tokens=[
            TokenLayer(
                symbols=[
                    SymbolLayer(chars=set(["1"]), s_class=AsciiClass.DIGIT, is_class=False),
                    SymbolLayer(chars=set(["2"]), s_class=AsciiClass.DIGIT, is_class=False),
                    SymbolLayer(chars=set(["3"]), s_class=AsciiClass.DIGIT, is_class=False),
                    SymbolLayer(chars=set(["4"]), s_class=AsciiClass.DIGIT, is_class=False),
                ]
            )
        ]
    )

    branch.add(
        "2234"
    )


    assert len(branch.tokens) == 1
    assert len(branch.tokens[0].symbols) == 4
    
    for i, symbol in enumerate(branch.tokens[0].symbols):
        assert symbol is not None
        assert not symbol.is_class
        assert symbol.s_class == AsciiClass.DIGIT
        
        if i != 0:
            assert len(symbol.chars) == 1

    assert len(branch.tokens[0].symbols[0].chars) == 2
