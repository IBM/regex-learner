import codecs
import pytest
from xsystem import XTructure
import pkg_resources # type: ignore

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

    list(map(x.learn_new_word, dataset))

    assert str(x)

    pattern = re.compile(str(x))

    for date in dataset:
        assert pattern.match(date), date


def test_ssn(faker):
    dataset = [
        faker.ssn() for _ in range(100)
    ]

    x = XTructure()

    list(map(x.learn_new_word, dataset))

    assert str(x)

    pattern = re.compile(str(x))

    for ssn in dataset:
        assert pattern.match(ssn), ssn


def test_optional_characters():
    x = XTructure()

    x.learn_new_word("ABCDE")
    x.learn_new_word("ABDE")

    assert len(x.branches) == 2


@pytest.mark.skip
def test_file_atc():
    x = XTructure()

    with open("common/atc.csv") as input:
        for line in input:
            line = line.strip()
            if len(line):
                x.learn_new_word(line)

    s = str(x)

    assert x


def test_realistic_data_account_id():
    with pkg_resources.resource_stream(__name__, "csv files/account.csv") as io_stream:
        data = codecs.getreader("utf8")(io_stream).readlines()

    assert len(data) == 2615

    rows = [line.strip().split(",") for line in data]

    lengths = [len(rows) for row in rows]

    assert min(lengths) == max(lengths)

    for i in range(len(rows[0])):
        x = XTructure()

        for row in rows:
            x.learn_new_word(row[i])
        
        print(x)

        assert str(x)