from xsystem import Branch
from xsystem import Token
from xsystem import Symbol
from xsystem import AsciiClass


def test_add():
    # examples: 1234

    branch = Branch(
        tokens=[
            Token(
                symbols=[
                    Symbol.build("1"),
                    Symbol.build("2"),
                    Symbol.build("3"),
                    Symbol.build("4"),
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
    b1 = Branch.build("ABC")
    b2 = Branch.build("CDE")

    assert b1.fit(b2) == b2.fit(b1)


def test_fit_score_same():
    b1 = Branch.build("ABC")
    b1_same = Branch.build("ABC")

    assert b1.fit(b1_same) == 0


def test_fit_score_of_similar_is_not_inf():
    b1 = Branch.build("ABC")
    b2 = Branch.build("123")

    assert b1.fit(b2) == 3

    b3 = Branch.build("AB1")

    assert b1.fit(b3) == 1

def test_merge_similar_length():
    b1 = Branch.build("ABC")
    b2 = Branch.build("123")

    b_merged = b1.merge(b2)

    assert b_merged is not None
    assert len(b_merged.tokens) == 1
    assert len(b_merged.tokens[0].symbols) == 3
