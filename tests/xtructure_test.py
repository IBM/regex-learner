from xsystem import XTructure
import pytest


@pytest.mark.skip
def test_working_example(faker):
    x = XTructure()

    for _ in range(100):
        d = faker.date(pattern=r"%d-%m-%Y")
        
        x.learn_new_word(d)