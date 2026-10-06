from dataclasses import dataclass
from ..raw.sentence import RawSentence
from .word import UDWord
from typing import Any, Iterator, Optional
from io import TextIOBase

@dataclass(frozen=True)
class UDSentence:
    raw: RawSentence
    words: list[UDWord]

    def __str__(self) -> str:
        return '\n'.join([str(self.raw)] + [str(word) for word in self.words])

    def __iter__(self) -> Iterator[UDWord]:
        return self.words.__iter__()

    def print_as_conllu(self, file: Optional[TextIOBase] = None) -> None:
        self.raw.print_as_conllu(file)
        print('\n', file=file)
        for word in self.words:
            word.print_as_conllu(file)
        print(3*'\n', file=file)

    def to_dict(self, source: str, url: str) -> dict[str, Any]:
        sentence_dict = self.raw.to_dict(source)
        sentence_dict['tokens'] = [word.to_dict() for word in self]
        sentence_dict['constituents'] = [word.to_constituent_dict() for word in self]
        sentence_dict['url'] = url
        return sentence_dict
