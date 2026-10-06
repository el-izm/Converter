from dataclasses import dataclass
from typing import Any, Optional
from io import TextIOBase

SENT_ATTRS = ['sent_id', 'text', 'segmentation', 'glosses', 'text_ru', 'title_n', 'title_r', 'genre', 'dialect', 'author', 'interviewer', 'date', 'source']

@dataclass(frozen=True)
class RawSentence:
    sent_id: str
    text: str
    text_ru: str
    MISC: str
    has_formatting_issue: bool
    glossed_text: str
    segmentation: str
    glosses: str
    title_n: str
    title_r: str
    genre: str
    dialect: str
    author: str
    interviewer: str
    date: str
    source: str


    def __str__(self) -> str:
        return '\n'.join([self.sent_id, self.text, self.text_ru, self.MISC])

    def print_as_conllu(self, file: Optional[TextIOBase] = None) -> None:
        for attr in SENT_ATTRS:
            print('# {0} = {1}'.format(attr, getattr(self, attr)), file=file)
        print('#MISC: {0}'.format(self.MISC), file=file)

    def to_dict(self, source: str) -> dict[str, Any]:
        return {
            'id': self.sent_id,
            'metadata': {
                'title_n': self.title_n,
                'title_r': self.title_r,
                'genre': self.genre,
                'dialect': self.dialect,
                'author': self.author,
                'interviewer': self.interviewer,
                'date': self.date,
                'source': self.source
            },
            'text': self.text,
            'segmented_text': self.segmentation,
            'glossed_text': self.glosses,
            # Если здесь будет приставка, которая у нас выделяется в отдельный токен, то длина будет на 1 меньше, чем кол-во токенов
            'length': len(self.segmentation.split()),
            'sentence_tree': '-',
            'russian_text': self.text_ru,
            'miscellaneous': self.MISC,
        }

    @property
    def numeric_id(self) -> int:
        first_line_number = self.sent_id.split('-', 1)[0]
        if first_line_number.isdigit():
            return int(first_line_number)
        else:
            return 0
