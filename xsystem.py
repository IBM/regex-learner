from __future__ import annotations
from argparse import ArgumentParser
import math

import sys

from dataclasses import dataclass
from dataclasses import field

from enum import Enum
from enum import auto
import re
from re import Pattern
from re import Match
from itertools import product
from typing import Generator
from typing import Optional
import string

ALPHA = 1/5
MAX_BRANCHES = 3
BRANCHING_THRESHORLD = .85

DELIMITERS=r"[-#.,]"


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


@dataclass
class SymbolLayer:
    s_class: AsciiClass
    chars: set[str]
    is_class: bool

    def d(self, s: str) -> float:
        if get_ascii_class(s) == self.s_class:
            return 0
        if not self.is_class and s in self.chars:
            return ALPHA
        return 1


def get_symbols_in_token(t: str) -> Generator[str, None, None]:
    for c in t:
        yield c


@dataclass
class TokenLayer:
    symbols: list[SymbolLayer] = field(default_factory=list)

    def d(self, t: str) -> float:
        return sum(
            symbol.d(tuple_element) for symbol, tuple_element in zip(self.symbols, get_symbols_in_token(t))
        ) + abs(
            len(t) - len(self.symbols)
        )


def get_token_in_tuple(t: str) -> Generator[str, None, None]:
    pattern: Pattern = re.compile(DELIMITERS)

    last_match: Optional[Match] = None

    for m in re.finditer(pattern, t):
        if last_match is None:
            yield t[:m.start()]
        else:
            yield t[last_match.end():m.start()]

        yield t[m.start():m.end()]

        last_match = m

    if last_match is None:
        yield t
    else:
        yield t[last_match.end():]


class NullTokenLayer(TokenLayer):
    def d(self, t: str) -> float:
        return 1.0 * len(t)


NULL_TOKEN = NullTokenLayer()


@dataclass
class BranchLayer:
    tokens: list[TokenLayer] = field(default_factory=list)

    def d(self, t: str) -> float:
        tokens: TokenLayer = [
            self.tokens[i] if i < len(self.tokens) else NULL_TOKEN for i, _ in enumerate(t)
        ]

        return sum(
            token.d(t_i) for token, t_i in zip(tokens, get_token_in_tuple(t))
        )

    def add(self, word: str) -> None:
        raise NotImplementedError()

    def fit_score(self, word: str) -> float:
        return self.d(word)


def get_class_characters(symbol_class: AsciiClass) -> set(str):
    if symbol_class == AsciiClass.ALNUM:
        return get_class_characters(AsciiClass.ALPHA) & get_ascii_class(AsciiClass.DIGIT)

    if symbol_class == AsciiClass.ALPHA:
        return get_class_characters(AsciiClass.UPPER) & get_ascii_class(AsciiClass.LOWER)

    if symbol_class == AsciiClass.BLANK:
        return set(" ", "\t")

    if symbol_class == AsciiClass.CNTRL:
        # CNTRL = auto(),  # Control characters. In ASCII, these characters have octal codes 000 through 037, and 177 (DEL). In other character sets, these are the equivalent characters, if any.
        raise ValueError()
        
    if symbol_class == AsciiClass.DIGIT:
        return set("0123456789")
    
    if symbol_class == AsciiClass.GRAPH:
        return get_class_characters(AsciiClass.ALPHA) & get_class_characters(AsciiClass.PUNCT)

    if symbol_class == AsciiClass.LOWER:
        return set("abcdefghijklmnopqrstuvwxyz")

    if symbol_class == AsciiClass.PRINT:
        return get_class_characters(AsciiClass.ALNUM) & get_class_characters(AsciiClass.PUNCT) & get_ascii_class(AsciiClass.SPACE)

    if symbol_class == AsciiClass.PUNCT:
        return "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~" 

    if symbol_class == AsciiClass.UPPER:
        return set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    if symbol_class == AsciiClass.XDIGIT:
        return set("0123456789ABCDEFabcdef")

    # SPACE = auto(),  # Space characters: in the ‘C’ locale, this is tab, newline, vertical tab, form feed, carriage return, and space. See Usage, for more discussion of matching newlines.
    if symbol_class == AsciiClass.SPACE:
        return set(
            "\t\n\x0B\x0C\x0D "
        )

    raise ValueError()



def build_new_symbol(symbol: str) -> SymbolLayer:
    symbol_class = get_ascii_class(symbol)
    return SymbolLayer(
        s_class=symbol_class,
        is_class=False,
        chars=set(symbol)
    )


def build_new_token(word: str) -> TokenLayer:
    return TokenLayer(
        list(build_new_symbol(symbol) for symbol in word)
    )


def build_new_branch(word: str) -> BranchLayer:
    return BranchLayer(
       tokens=[
        build_new_token(token) for token in get_token_in_tuple(word)
       ] 
    )


def merge_most_similar(branches: list[BranchLayer]) -> list[BranchLayer]:
    raise NotImplementedError()


@dataclass
class XTructure:
    branches: list[BranchLayer] = field(default_factory=list)

    def d(self, t: tuple[str, ...]) -> float:
        return min(b.d(t) for b in self.branches)

    def learn_new_word(self, word: str) -> None:
        if not len(self.branches):
            self.branches.append(build_new_branch(word))
        else:
            best_branch = self._best_branch(word)

            if best_branch.d(word) < BRANCHING_THRESHORLD:
                best_branch.add(word)
            else:
                self.branches.append(
                    build_new_branch(word)
                )

        if len(self.branches) > MAX_BRANCHES:
            self.branches = merge_most_similar(self.branches)

    def _best_branch(self, word: str) -> BranchLayer:
        best_score = math.inf
        best_branch: Optional[BranchLayer] = None

        for branch in self.branches:
            branch_score = branch.fit_score(word)

            if branch_score < best_score:
                best_branch = branch

        return best_branch


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="",
        description="",
    )

    return parser



def main() -> int:
    with open(sys.argv[1], encoding="utf-8") as input:
        raise NotImplementedError()

    return 0


if __name__ == "__main__":
    raise SystemError(main())