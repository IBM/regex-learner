from xsystem import XTructure

import re


def test_working_example_single_branch(faker):
    x = XTructure()

    for _ in range(100):
        d = faker.date(pattern=r"%d-%m-%Y")
        
        x.learn_new_word(d)

    assert x
    assert len(x.branches) == 1
    assert len(x.branches[0].tokens) == 5
    assert len(x.branches[0].tokens[0].symbols) == 2
    assert len(x.branches[0].tokens[1].symbols) == 1
    assert len(x.branches[0].tokens[2].symbols) == 2
    assert len(x.branches[0].tokens[3].symbols) == 1
    assert len(x.branches[0].tokens[4].symbols) == 4


def test_working_example_multiple_branch():
    x = XTructure()

    x.learn_new_word("2022-12-25")
    x.learn_new_word("N/A")

    assert x
    assert len(x.branches) == 2


def test_learnt_pattern(faker):
    dataset = [
        date for date in faker.date(pattern=r"%d-%m-%Y")
    ]

    x = XTructure()

    map(x.learn_new_word, dataset)

    pattern = re.compile(str(x))

    for date in dataset:
        assert pattern.match(date), date
