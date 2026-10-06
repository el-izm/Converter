import re
import warnings
from io import TextIOBase, StringIO
from .. import EMPTY_FIELD_MARKER
from ..model.raw.sentence import RawSentence
from ..model.glossing.sentence import GlossedSentence
from ..model.glossing.word import GlossedWord
from ..model.glossing.auxiliary import preprocess_token
from .tokenizer import Tokenizer
from .attribution_remover import AttributionRemover
from .token_filter import TokenFilter
from .auxiliary import is_empty_or_comment, format_line_number, construct_words, normalize_token, normalize_gloss, unsegment_word
WARNING_PREFIX = '# WARNING: '
from ..normalisation.translation import normalise_translation

class SentenceParser():
    title_n: str = ''
    title_r: str = ''
    genre: str = ''
    dialect: str = ''
    author: str = ''
    interviewer: str = ''
    date: str = ''
    source: str = ''
    _in_metadata: bool = True

    def _parse_metadata_line(self, line: str) -> bool:
        if '=' in line:
            parts = line.split('=', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                
                if key == 'title_n':
                    self.title_n = value
                elif key == 'title_r':
                    self.title_r = value
                elif key == 'genre':
                    self.genre = value
                elif key == 'dialect':
                    self.dialect = value
                elif key == 'author':
                    self.author = value
                elif key == 'interviewer':
                    self.interviewer = value
                elif key == 'date':
                    self.date = value
                elif key == 'source':
                    self.source = value
                else:
                    return False
                return True
        return False

    def read_sentence_from_stream(self, stream: TextIOBase) -> GlossedSentence | None:
        """Reads the first glossed sentence from a text stream

        :param stream: A text stream yielding the liens of a glossed text one by one
        :raises ValueError: No translation was given for the glossed sentence
        :return: A Sentence object representing the first glossed sentence if there are any glossed sentences in the file, None otherwise
        """
        sentence_words = list[GlossedWord]()
        # The next variable stores the tokens of the current line.
        line_tokens: list[str] | None = None
        # We need this variable outside of the loop for error messages.
        line_id = "unknown"
        # To print the glossed sentence to the skipped sentences file if it has a formatting issue
        glossed_text = StringIO()
        has_formatting_issue = False
        for line in stream:
            line = line.strip()

            if self._in_metadata:
                if self._parse_metadata_line(line):
                    continue
                else:
                    self._in_metadata = False

            if not line.startswith(WARNING_PREFIX):
                print(line, file=glossed_text)
            if not is_empty_or_comment(line):
                split = re.split("\t| ", line, 1)
                if len(split) < 2:
                    has_formatting_issue = True
                    message = "A line is not numbered: {0}".format(line)
                    warnings.warn(message)
                    print(WARNING_PREFIX + message, file=glossed_text)
                    continue
                line_id, line_body = split
                line_number = line_id[0:-1]
                line_type = line_id[-1]
                if "@" in line_number:
                    continue
                if not line_number or not line_number[0].isdigit():
                    has_formatting_issue = True
                    message = "A line has an invalid identifier: {0}".format(line)
                    warnings.warn(message)
                    print(WARNING_PREFIX + message, file=glossed_text)
                    continue
                if line_number[0].isdigit():
                    match line_type:
                        # Token line
                        case ">":
                            line_tokens = Tokenizer.tokenize(line)[1:]
                            line_tokens = [normalize_token(t) for t in line_tokens]
                            line_tokens = AttributionRemover.remove_attribution(line_tokens)
                            line_tokens = TokenFilter.filter_tokens(line_tokens)
                        # Gloss line
                        case "<":
                            glosses = Tokenizer.tokenize(line)[1:]
                            glosses = [normalize_gloss(g) for g in glosses]
                            glosses = AttributionRemover.remove_attribution(glosses)
                            if line_tokens is None:
                                has_formatting_issue = True
                                print(WARNING_PREFIX + "The gloss line {0} has no corresponding token line.".format(line_id),
                                    file=glossed_text)
                                line_tokens = [EMPTY_FIELD_MARKER] * len(glosses)
                            elif len(glosses) < len(line_tokens):
                                has_formatting_issue = True
                                print(WARNING_PREFIX + "The gloss line {0} has fewer tokens than the corresponding token line.".format(line_id),
                                    file=glossed_text)
                                glosses = [EMPTY_FIELD_MARKER] * len(line_tokens)
                            elif len(glosses) > len(line_tokens):
                                has_formatting_issue = True
                                print(WARNING_PREFIX + "The gloss line {0} has more tokens than the corresponding token line.".format(line_id),
                                    file=glossed_text)
                                glosses = [EMPTY_FIELD_MARKER] * len(line_tokens)
                            line_words = construct_words(line_tokens, glosses)
                            sentence_words.extend(line_words)
                        # Translation line
                        case "=":
                            sent_id = format_line_number(line_number)
                            text_tokens = [unsegment_word(word.segmentation) for word in sentence_words]
                            text_tokens = [t for t in text_tokens if t != ""]
                            text = " ".join(text_tokens)
                            translation_tokens = line_body.split(" ")
                            translation_tokens = AttributionRemover.remove_attribution(translation_tokens)
                            text_ru = normalise_translation(" ".join(translation_tokens))
                            MISC = ""
                            segmented_words = " ".join([word.segmentation for word in sentence_words])
                            glossed_words = " ".join([word.gloss for word in sentence_words])
                            raw_sentence = raw_sentence = RawSentence(
                                sent_id=sent_id,
                                text=text,
                                text_ru=text_ru,
                                MISC=MISC,
                                has_formatting_issue=has_formatting_issue,
                                glossed_text=glossed_text.getvalue(),
                                segmentation=segmented_words,
                                glosses=glossed_words,
                                title_n=self.title_n,
                                title_r=self.title_r,
                                genre=self.genre,
                                dialect=self.dialect,
                                author=self.author,
                                interviewer=self.interviewer,
                                date=self.date,
                                source=self.source
                            )
                            return GlossedSentence(raw_sentence, sentence_words)

        if (len(sentence_words) == 0):
            return None
        else:
            raise ValueError("No translation was provided for the sentence ending on line {0}".format(line_id))
