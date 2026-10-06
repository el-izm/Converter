import re
from re import Pattern

class Tokenizer:
    """A simple whitespace tokenizer preserving trailing punctuation.
    This class is static, no instances of it should be created.
    """
    pattern: Pattern[str] = re.compile("[\t ]+")

    @classmethod
    def tokenize(cls, line: str) -> list[str]:
        """Splits a line of a text into an array of words on whitespace,
        preserving trailing punctuation.

        :param line: The line to split
        :return: An array of words
        """
        tokens: list[str] = cls.pattern.split(line)
        return tokens
