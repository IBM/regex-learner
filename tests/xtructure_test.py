from xsystem import XTructure


def test_working_example_single_branch(faker):
    x = XTructure()

    for _ in range(100):
        d = faker.date(pattern=r"%d-%m-%Y")
        
        x.learn_new_word(d)

    assert x
    assert len(x.branches) == 1
    assert len(x.branches[0].tokens) == 8


def test_working_example_multiple_branch():
    x = XTructure()

    x.learn_new_word("2022-12-25")
    x.learn_new_word("N/A")


