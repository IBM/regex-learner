from xsystem import Branch
from xsystem import Token
from xsystem import Symbol
from xsystem import AsciiClass


def test_add():
    # branch for "\d{4}"
    # examples: 1234

    branch = Branch(
        tokens=[
            Token(
                symbols=[
                    Symbol(chars=set(["1"]), a_class=AsciiClass.DIGIT, is_class=False),
                    Symbol(chars=set(["2"]), a_class=AsciiClass.DIGIT, is_class=False),
                    Symbol(chars=set(["3"]), a_class=AsciiClass.DIGIT, is_class=False),
                    Symbol(chars=set(["4"]), a_class=AsciiClass.DIGIT, is_class=False),
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
        assert symbol.a_class == AsciiClass.DIGIT
        
        if i != 0:
            assert len(symbol.chars) == 1

    assert len(branch.tokens[0].symbols[0].chars) == 2


def test_fit_score_simmetric():
    "ABC"
    b1 = Branch.build("ABC")
    b2 = Branch.build("CDE")

    assert b1.fit(b2) == b2.fit(b1)