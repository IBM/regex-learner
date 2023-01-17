from __future__ import annotations
from argparse import ArgumentParser

import sys
import csv

from dataclasses import dataclass
from dataclasses import field

from enum import Enum
from enum import auto
from re import compile
from itertools import product
from typing import Generator

ALPHA = 1/5
MAX_BRANCHES = 3
BRANCHING_THRESHORLD = .85


class AsciiClass(Enum):
    ALNUM = auto(),  # Alphanumeric characters: ‘[:alpha:]’ and ‘[:digit:]’; in the ‘C’ locale and ASCII character encoding, this is the same as ‘[0-9A-Za-z]’.
    ALPHA = auto(),  # Alphabetic characters: ‘[:lower:]’ and ‘[:upper:]’; in the ‘C’ locale and ASCII character encoding, this is the same as ‘[A-Za-z]’.
    BLANK = auto(),  # Blank characters: space and tab.
    CNTRL = auto(),  # Control characters. In ASCII, these characters have octal codes 000 through 037, and 177 (DEL). In other character sets, these are the equivalent characters, if any.
    DIGIT = auto(),  # Digits: 0 1 2 3 4 5 6 7 8 9.
    GRAPH = auto(),  # Graphical characters: ‘[:alnum:]’ and ‘[:punct:]’.
    LOWER = auto(),  # Lower-case letters; in the ‘C’ locale and ASCII character encoding, this is a b c d e f g h i j k l m n o p q r s t u v w x y z.
    PRINT = auto(),  # Printable characters: ‘[:alnum:]’, ‘[:punct:]’, and space.
    PUNCT = auto(),  # Punctuation characters; in the ‘C’ locale and ASCII character encoding, this is ! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ ` { | } ~.
    SPACE = auto(),  # Space characters: in the ‘C’ locale, this is tab, newline, vertical tab, form feed, carriage return, and space. See Usage, for more discussion of matching newlines.
    UPPER = auto(),  # Upper-case letters: in the ‘C’ locale and ASCII character encoding, this is A B C D E F G H I J K L M N O P Q R S T U V W X Y Z.
    XDIGIT = auto(),  # Hexadecimal digits: 0 1 2 3 4 5 6 7 8 9 A B C D E F a b c d e f.


def get_ascii_class(s: str) -> AsciiClass:
    if len(s) > 1:
        raise ValueError("Expected single character")

    if s.isdigit():
        return AsciiClass.DIGIT

    if s.isalpha():
        if s.islower():
            return AsciiClass.LOWER
        elif s.isupper():
            return AsciiClass.UPPER
        raise ValueError(f"{s} is ALPHA but neither lower or upper")

    if s.isspace():
        return AsciiClass.SPACE
    
    if s.isprintable():
        return AsciiClass.PUNCT

    raise ValueError(f"{s} unknown")


class SymbolLayer:
    s_class: AsciiClass
    chars: set[str]
    is_class: bool

    def d_i(self, s: str) -> float:
        if get_ascii_class(s) == self.s_class:
            return 1
        if s in self.chars:
            return ALPHA
        return 0



def get_symbols_in_token(t: str) -> Generator[str, None, None]:
    for c in t:
        yield c


@dataclass
class TokenLayer:
    symbols: list[SymbolLayer] = field(default_factory=list)

    def d(self, t: str) -> float:
        return sum(
            l_i.d(t_i) for l_i, t_i in product(self.symbols, get_symbols_in_token(t))
        ) + abs(
            len(t) - len(self.symbols)
        )


def get_token_in_tuple(t: tuple[str, ...]) -> Generator[str, None, None]:
    raise NotImplementedError()


@dataclass
class BranchLayer:
    K: list[TokenLayer] = field(default_factory=list)

    def d(self, t: tuple[str, ...]) -> float:
        return sum(
            k.d(t_i) for k, t_i in product(self.K, get_token_in_tuple(t))
        )


@dataclass
class XTructure:
    B: list[BranchLayer] = field(default_factory=list)

    def d(self, t: tuple[str, ...]) -> float:
        return min(b.d(t) for b in self.B)


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="",
        description="",
    )

    return parser



def main() -> int:
    with open(sys.argv[1], encoding="utf-8") as input:
        pass

    return 0


if __name__ == "__main__":
    raise SystemError(main())