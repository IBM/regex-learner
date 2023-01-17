from xsystem import get_token_in_tuple
from xsystem import build_new_token

def test_token_fit_score():
    pass


def test_tokenization_one_item():
    tokens = list(get_token_in_tuple("abcd"))

    assert tokens is not None
    assert len(tokens) == 1
    assert tokens[0] == "abcd"


def test_tokenization_function():
    example = "2023-10-11"

    tokens = list(get_token_in_tuple(example))

    assert tokens is not None
    assert len(tokens) == 5
    assert tokens[0] == "2023"
    assert tokens[1] == "-"
    assert tokens[2] == "10"
    assert tokens[3] == "-"
    assert tokens[4] == "11"


def test_token_createion():
    token = build_new_token("2023")

    assert token
    assert len(token.symbols) == 4
