from dataclasses import dataclass
from ... import EMPTY_FIELD_MARKER, MORPHOSYNTACTIC_PROPERTY_SEPARATOR
from typing import Any, Optional
from io import TextIOBase

# Attributes to include in conllu
WORD_ATTRS = ['word_id', 'form', 'lemma', 'upos', 'xpos', 'feats', 'head', 'deprel', 'deps', 'translation']

@dataclass(order=True, frozen=True)
class UDWord:
    word_id: str
    form: str
    lemma: str
    segmentation: str
    gloss: str
    upos: str
    feats: str
    translation: str
    xpos: str = EMPTY_FIELD_MARKER
    head: str = EMPTY_FIELD_MARKER
    deprel: str = EMPTY_FIELD_MARKER
    deps: str = EMPTY_FIELD_MARKER

    def __str__(self) -> str:
        return '{0:10} {1:10} {2:10} {3:10} {4}'.format(
            self.form, self.lemma, self.upos, self.translation, self.feats
        )

    def print_as_conllu(self, file: Optional[TextIOBase] = None) -> None:
        values = [getattr(self, attr) for attr in WORD_ATTRS]
        line = "\t".join(values)
        print(line, file=file)

    @property
    def tagset(self) -> list[str]:
      tagset = [self.upos]
      if self.feats != EMPTY_FIELD_MARKER:
        feat_vals = self.feats.split(MORPHOSYNTACTIC_PROPERTY_SEPARATOR)
        tagset.extend(feat_vals)
      return tagset

    def to_dict(self) -> dict[str, Any]:
        return {
            'itoken': int(self.word_id),
            'token': self.form,
            'lemma': self.lemma,
            'segmentation': self.segmentation,
            'gloss': self.gloss,
            'tagsets': [self.tagset],
            'parent_token_index': '-',
            'edge_type': '-',
            'constituent': {"name": "-", "is_head": False, "id": "-"},
            'translation': self.translation
        }

    def to_constituent_dict(self) -> dict[str, Any]:
        return {
            'name': '-',
            'id': int(self.word_id),
            'tags': self.tagset,
            'tokens': [[self.form]],
            'head_id': '-',
            'text': self.form,
            'length': 1
        }
