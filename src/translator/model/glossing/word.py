from dataclasses import dataclass
from .auxiliary import is_lat, is_cyr, preprocess_token
from ..ud.word import UDWord
from ...conversion.lemma_detection import lemmas_gram
from ...part_of_speech import define_pos_tag
from ...conversion.properties import get_feats
from ... import EMPTY_FIELD_MARKER, MORPHOSYNTACTIC_PROPERTY_SEPARATOR
from ...atr_val import prefixes as language_has_prefixes
from itertools import chain
from warnings import warn
from logging import getLogger
logger = getLogger(__name__)

def join_feats(feat_array: list[str]) -> str:
  if len(feat_array) > 0:
    return MORPHOSYNTACTIC_PROPERTY_SEPARATOR.join(feat_array)
  else:
    return EMPTY_FIELD_MARKER

@dataclass(order=True, frozen=True)
class GlossedWord:
    segmentation: str
    gloss: str

    def __str__(self) -> str:
        return '{0:25} {1}'.format(self.segmentation, self.gloss)

    @property
    def has_proclitic(self) -> bool:
        gloss = self.gloss
        first_tag = gloss.split("-")[0]
        return (any(is_lat(char) for char in first_tag) and
                # Добавлено, чтобы не выделять хваршинские основы как проклитики
                not any(is_cyr(char) for char in first_tag) and
                len(gloss.split("-")) > 1 and
                any(is_cyr(char) for char in gloss))

    def to_UD_words(self, word_id: int=0) -> list[UDWord]:
        segmentation = self.segmentation
        gloss = self.gloss
        UD_words = list[UDWord]()
        try:
            lem1, gram1 = lemmas_gram(segmentation, gloss)
        except (IndexError, ValueError) as exc:
            warn('lemmas_gram raised\n{0}\non word "{1}" glossed as "{2}".'
                  .format(repr(exc), self.segmentation, self.gloss))
            logger.error('{0:30} {1}'.format(self.segmentation, self.gloss))
            lem1 = []
            gram1 = []
        lemma = lem1[0] if len(lem1) > 0 else 'None'
        upos_tag = define_pos_tag(lem1[-1]) if len(lem1) > 0 else ["None"]
        translation = lem1[-1] if len(lem1) > 0 else 'None'
        if not language_has_prefixes and self.has_proclitic:
            clitic_form, segmented_word_form = segmentation.split("-", 1)
            clitic_gram = gram1[0]
            word_gram = list(chain.from_iterable(gram1[1:]))
            clitic_lemma = clitic_form
            clitic_upos = "PART"
            clitic_feat_array, _ = get_feats(clitic_gram, [clitic_upos])
            clitic_feat_array.append("Clitic=Yes")
            clitic_feat_string = join_feats(clitic_feat_array)
            clitic_translation = gloss.split("-")[0]
            clitic = UDWord(str(word_id), clitic_form, clitic_lemma, clitic_form, clitic_translation, clitic_upos, clitic_feat_string, clitic_translation)
            UD_words.append(clitic)
            word_id += 1
            word_form = preprocess_token(segmented_word_form)
            word_segmentation = segmented_word_form
            word_gloss = "-".join(gloss.split("-")[1:])
        else:
            word_form = preprocess_token(segmentation)
            word_gram = list(chain.from_iterable(gram1))
            word_segmentation = self.segmentation
            word_gloss = self.gloss
        word_feat_array, upos = get_feats(word_gram, upos_tag)
        word_feat_string = join_feats(word_feat_array)
        word = UDWord(str(word_id), word_form, lemma, word_segmentation, word_gloss, upos, word_feat_string, translation)
        UD_words.append(word)
        return UD_words
