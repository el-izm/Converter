from ..model.glossing.auxiliary import PUNCTUATION
from ..model.glossing.word import GlossedWord

LAT_TO_CYR = str.maketrans('aeoyxcp', 'аеоухср')
CYR_TO_LAT = str.maketrans('АЕОКВТМХСР', 'AEOKBTMXCP')

def normalize_token(word: str) -> str:
  return word.translate(LAT_TO_CYR)

def normalize_gloss(word: str) -> str:
  return word.translate(LAT_TO_CYR).translate(CYR_TO_LAT)

def is_empty_or_comment(line: str) -> bool:
  """Determines whether a line of a file containing a glossed text is empty or comment.

  :param line: The line to inspect
  :return: True if the given line is empty or comment, False otherwise
  """
  return line == "" or line.startswith("#") or line.startswith("@")

def delete_punctuation(word: str) -> str:
  """Функция, которая убирает пунктуационные знаки в конце и в начале слов.
  """
  if (word != "") and (word != " "):
    word = word.strip('''“!,.;"'()«…»''')
    return word
  else:
    return word
  
def unsegment_word(segmentation: str) -> str:
  morphs = segmentation.split('-')
  morphs = [m for m in morphs if m != '0']
  return ''.join(morphs)

def construct_words(tokens: list[str], glosses: list[str]) -> list[GlossedWord]:
  words = []
  in_parenthetical = False
  for token, gloss in zip(tokens, glosses, strict=True):
    if token.startswith('('):
      in_parenthetical = True
    if in_parenthetical:
      if ')' in token:
        in_parenthetical = False
      continue
    words.append(GlossedWord(delete_punctuation(token), delete_punctuation(gloss)))
  return words

def format_line_number(line_number: str) -> str:
    if "_" not in line_number:
        sent_id = line_number
    else:
        # "To split" is an irregular verb. The simple past and past participle is "split".
        split_number = line_number.split("_")
        sent_id = "{0}-{1}".format(split_number[0], split_number[-1])
    return sent_id
