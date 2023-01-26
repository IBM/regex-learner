from __future__ import annotations
from argparse import ArgumentParser, Namespace
from itertools import combinations
import math

import sys
import string

from dataclasses import dataclass
from dataclasses import field

from enum import Enum
from enum import auto
import re
from re import Match
from re import Pattern
from typing import Generator
from typing import Optional


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
    ANY = auto(),

    @staticmethod
    def get_parent(cls: AsciiClass) -> Optional[AsciiClass]:
        if cls == AsciiClass.ALNUM:
            return AsciiClass.GRAPH
        if cls == AsciiClass.ALPHA:
            return AsciiClass.ALNUM
        if cls == AsciiClass.BLANK:
            return AsciiClass.SPACE
        if cls == AsciiClass.DIGIT:
            return AsciiClass.ALNUM
        if cls == AsciiClass.GRAPH:
            return AsciiClass.PRINT
        if cls == AsciiClass.LOWER:
            return AsciiClass.ALPHA
        if cls == AsciiClass.PRINT:
            return AsciiClass.ANY
        if cls == AsciiClass.PUNCT:
            return AsciiClass.GRAPH
        if cls == AsciiClass.SPACE:
            return AsciiClass.PRINT
        if cls == AsciiClass.UPPER:
            return AsciiClass.ALPHA
        if cls == AsciiClass.CNTRL:
            return AsciiClass.ANY
        if cls == AsciiClass.XDIGIT:
            return AsciiClass.ALNUM
        if cls == AsciiClass.ANY:
            return None

        raise ValueError(f"Unknown ASCII class {cls}")

    @staticmethod
    def get_ascii_class_pattern(cls: AsciiClass) -> str:
        if cls == AsciiClass.ALNUM:
            return r"[:alnum:]"
        if cls == AsciiClass.ALPHA:
            return r"[:alpha:]"
        if cls == AsciiClass.BLANK:
            return r"[:blank:]"
        if cls == AsciiClass.CNTRL:
            return r"[:cntrl:]"
        if cls == AsciiClass.DIGIT:
            return r"[0-9]"
        if cls == AsciiClass.GRAPH:
            return r"[:graph:]"
        if cls == AsciiClass.LOWER:
            return r"[:lower:]"
        if cls == AsciiClass.PRINT:
            return r"[:print:]"
        if cls == AsciiClass.PUNCT:
            return r"[:punct:]"
        if cls == AsciiClass.SPACE:
            return r"[:space:]"
        if cls == AsciiClass.UPPER:
            return r"[:upper:]"
        if cls == AsciiClass.XDIGIT:
            return r"[:xdigit:]"
        if cls == AsciiClass.ANY:
            return r"."
        raise ValueError(f"Unsupported ASCII class {cls}")

    @staticmethod
    def get_class_characters(symbol_class: AsciiClass) -> set[str]:
        if symbol_class == AsciiClass.ALNUM:
            return AsciiClass.get_class_characters(AsciiClass.ALPHA) & AsciiClass.get_class_characters(AsciiClass.DIGIT)

        if symbol_class == AsciiClass.ALPHA:
            return AsciiClass.get_class_characters(AsciiClass.UPPER) & AsciiClass.get_class_characters(AsciiClass.LOWER)

        if symbol_class == AsciiClass.BLANK:
            return set([" ", "\t"])

        if symbol_class == AsciiClass.CNTRL:
            # CNTRL = auto(),  # Control characters. In ASCII, these characters have octal codes 000 through 037, and 177 (DEL). In other character sets, these are the equivalent characters, if any.
            raise ValueError()

        if symbol_class == AsciiClass.DIGIT:
            return set(string.digits)

        if symbol_class == AsciiClass.GRAPH:
            return AsciiClass.get_class_characters(AsciiClass.ALPHA) & AsciiClass.get_class_characters(AsciiClass.PUNCT)

        if symbol_class == AsciiClass.LOWER:
            return set(string.ascii_lowercase)

        if symbol_class == AsciiClass.PRINT:
            return AsciiClass.get_class_characters(AsciiClass.ALNUM) & AsciiClass.get_class_characters(AsciiClass.PUNCT) & AsciiClass.get_class_characters(AsciiClass.SPACE)

        if symbol_class == AsciiClass.PUNCT:
            return set(string.punctuation)

        if symbol_class == AsciiClass.UPPER:
            return set(string.ascii_uppercase)

        if symbol_class == AsciiClass.XDIGIT:
            return set(string.hexdigits)

        if symbol_class == AsciiClass.SPACE:
            return set(
                # "\t\n\x0B\x0C\x0D "
                string.whitespace
            )

        raise ValueError()

    @staticmethod
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
            return AsciiClass.ALPHA

        if s.isspace():
            return AsciiClass.SPACE

        if s.isprintable():
            return AsciiClass.PUNCT

        raise ValueError(f"{s} unknown")

    @staticmethod
    def find_common_ancestor(class1: AsciiClass, class2: AsciiClass) -> AsciiClass:
        parent: Optional[AsciiClass] = class1
        ancestors: set[AsciiClass] = {class1}

        assert parent is not None

        while True:
            parent = AsciiClass.get_parent(parent)
            if parent is None:
                break
            ancestors.add(parent)

        parent = class2
        while parent is not None:
            if parent in ancestors:
                return parent
            else:
                parent = AsciiClass.get_parent(parent)

        if parent is None:
            return AsciiClass.ANY

        raise ValueError()


@dataclass
class Symbol:
    a_class: AsciiClass
    chars: set[str]
    is_class: bool
    is_optional: bool = False

    def fit_score(self, s: str, alpha: float) -> float:
        if AsciiClass.get_ascii_class(s) == self.a_class:
            return 0
        if not self.is_class and s in self.chars:
            return alpha
        return 1

    def __str__(self) -> str:
        if self.is_class:
            return AsciiClass.get_ascii_class_pattern(self.a_class)
        elif len(self.chars) == 1:
            return self._sanitize(next(iter(self.chars))) + ("?" if self.is_optional else "")
        else:
            return "[" + "".join(Symbol._sanitize(c) for c in self.chars) + "]" + ("?" if self.is_optional else "")

    def fit(self, other: Symbol) -> float:
        if self.a_class == other.a_class:
            return 0
        if AsciiClass.find_common_ancestor(self.a_class, other.a_class) == other.a_class:
            return 0
        if AsciiClass.find_common_ancestor(self.a_class, other.a_class) == self.a_class:
            return 0

        common_chars = len(self.chars & other.chars)
        if common_chars != 0:
            return 1 - common_chars / len(self.chars)
        else:
            return 1

    @staticmethod
    def _sanitize(c: str) -> str:
        if c in ".^$*+?()[{\\|":
            return f"\\{c}"
        return c

    def merge(self, other: Symbol) -> Symbol:
        if other.a_class != self.a_class:
            na_class = AsciiClass.find_common_ancestor(other.a_class, self.a_class)
        else:
            na_class = self.a_class

        chars = self.chars | other.chars

        return Symbol(
            na_class,
            chars=chars,
            is_class=len(chars) == len(AsciiClass.get_class_characters(na_class))
        )

    @staticmethod
    def build(symbol: str) -> Symbol:
        symbol_class = AsciiClass.get_ascii_class(symbol)
        return Symbol(
            a_class=symbol_class,
            is_class=False,
            chars=set(symbol)
        )


@dataclass
class Token:
    symbols: list[Symbol] = field(default_factory=list)
    optional: bool = False

    def fit_score(self, t: str, alpha: float) -> float:
        return sum(
            symbol.fit_score(tuple_element, alpha) for symbol, tuple_element in zip(self.symbols, Token.get_symbols_in_token(t))
        ) + abs(
            len(t) - len(self.symbols)
        )

    def merge(self, other: Token) -> Token:
        symbols = [symbol.merge(other_symbol) for symbol, other_symbol in zip(self.symbols, other.symbols)]

        if len(self.symbols) == len(other.symbols):
            return Token(symbols=symbols, optional=self.optional or other.optional)
        elif len(self.symbols) > len(other.symbols):
            missing = [Symbol(s.a_class, s.chars, s.is_class, True) for s in self.symbols[len(other.symbols):]]
        else:
            missing = [Symbol(s.a_class, s.chars, s.is_class, True) for s in other.symbols[len(self.symbols):]]

        return Token(symbols=symbols + missing, optional=self.optional or other.optional)

    def fit(self, other: Token) -> float:
        return sum(
            symbol.fit(other_symbol) for symbol, other_symbol in zip(self.symbols, other.symbols)
        ) + abs(len(self.symbols) - len(other.symbols))

    @staticmethod
    def get_symbols_in_token(t: str) -> Generator[str, None, None]:
        for c in t:
            yield c

    def __str__(self) -> str:
        return "(" + "".join(str(symbol) for symbol in self.symbols) + ")" + ("?" if self.optional else "")

    @staticmethod
    def build(word: str) -> Token:
        return Token(
            list(Symbol.build(symbol) for symbol in word)
        )


class NullToken(Token):
    def d(self, t: str) -> float:
        return 1.0 * len(t)


@dataclass
class Branch:
    tokens: list[Token] = field(default_factory=list)

    def fit_score(self, t: str, alpha: float) -> float:
        tokens: list[Token] = [self.tokens[i] if i < len(self.tokens) else NullToken() for i, _ in enumerate(t)]

        return sum(
            token.fit_score(t_i, alpha) for token, t_i in zip(tokens, Branch.get_tokens_in_tuple(t))
        )

    def add(self, word: str) -> None:
        self.tokens = [token.merge(nt) for nt, token in zip(Branch.build(word).tokens, self.tokens)]

    def __str__(self) -> str:
        return "".join(str(token) for token in self.tokens)

    def fit(self, other: Branch) -> float:
        return sum(
            token.fit(other_token) for token, other_token in zip(self.tokens, other.tokens)
        ) + abs(len(self.tokens) - len(other.tokens))

    def merge(self, other: Branch) -> Branch:
        tokens = [
            token.merge(other_token) for token, other_token in zip(self.tokens, other.tokens)
        ]

        if len(self.tokens) == len(other.tokens):
            return Branch(tokens)
        elif len(self.tokens) > len(other.tokens):
            missing = [
                Token(token.symbols, True) for token in self.tokens[len(other.tokens):]
            ]

            assert len(tokens) + len(missing) == len(self.tokens)
        else:
            missing = [
                Token(token.symbols, True) for token in other.tokens[len(self.tokens):]
            ]

            assert len(tokens) + len(missing) == len(other.tokens)

        return Branch(tokens + missing)

    @staticmethod
    def get_tokens_in_tuple(t: str, delimiters: str = r"[-_/\\#., ]") -> Generator[str, None, None]:
        pattern: Pattern[str] = re.compile(delimiters)

        last_match: Optional[Match[str]] = None

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

    @staticmethod
    def build(word: str) -> Branch:
        return Branch(
            tokens=[
                Token.build(token) for token in Branch.get_tokens_in_tuple(word)
            ]
        )

    def __repr__(self) -> str:
        return f"Branch[{str(self)}"


@dataclass
class XTructure:
    alpha: float = 1 / 5
    max_branches: int = 8
    branching_threshold: float = 0.85

    branches: list[Branch] = field(default_factory=list)

    def fit_score(self, t: str) -> float:
        return min(b.fit_score(t, self.alpha) for b in self.branches)

    def learn_new_word(self, word: str) -> bool:
        if len(word) == 0:
            return False

        if not len(self.branches):
            self.branches.append(Branch.build(word))

        else:
            best_branch, score = self._best_branch(word)

            if score < self.branching_threshold:
                best_branch.add(word)
            else:
                self.branches.append(
                    Branch.build(word)
                )

            if len(self.branches) > self.max_branches:
                self.branches = self.merge_most_similar()

        return True

    def _best_branch(self, word: str) -> tuple[Branch, float]:
        assert len(self.branches)

        best_score = math.inf
        best_branch: Optional[Branch] = None

        for branch in self.branches:
            branch_score = branch.fit_score(word, self.alpha)

            if branch_score < best_score:
                best_branch = branch
                best_score = branch_score

        assert best_branch is not None
        assert best_score != math.inf

        return best_branch, best_score

    def merge_most_similar(self) -> list[Branch]:
        min_distance = math.inf
        m_bi: Optional[Branch] = None
        m_bj: Optional[Branch] = None

        for bi, bj in combinations(self.branches, 2):
            assert bi is not bj

            distance = bi.fit(bj)

            if distance < min_distance:
                min_distance = distance
                m_bi = bi
                m_bj = bj

        assert m_bi is not None
        assert m_bj is not None

        self.branches.remove(m_bi)
        self.branches.remove(m_bj)

        self.branches.append(m_bi.merge(m_bj))

        return self.branches

    def __str__(self) -> str:
        return "|".join(str(branch) for branch in self.branches)


def parse_arguments() -> Namespace:
    parser = ArgumentParser(
        prog=sys.argv[0].split("/")[-1],
        description="A simple tool to learn human readable a regular expression from examples",
    )

    parser.add_argument("-i", "--input", help="Path to the input source, defaults to stdin")
    parser.add_argument("-o", "--output", help="Path to the output file, defaults to stdout")
    parser.add_argument("--max-branch", type=int, default=8, help="Maximum number of branches allowed, defaults to 8")
    parser.add_argument("--alpha", type=float, default=1 / 5, help="Weight for fitting tuples, defaults to 1/5")
    parser.add_argument("--branch-threshold", type=float, default=.85, help="Branching threshold, defaults to 0.85, relative to the fitting score alpha")

    return parser.parse_args()


def main() -> int:
    cmd = parse_arguments()

    x = XTructure(
        cmd.alpha,
        cmd.max_branch,
        cmd.branch_threshold
    )

    data_source = open(cmd.input) if cmd.input else sys.stdin

    for line in data_source:
        x.learn_new_word(line.strip())

    output = open(cmd.output) if cmd.output else sys.stdout

    print(str(x), file=output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
