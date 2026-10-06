from itertools import filterfalse
from typing import Iterable

MORPH_BOUNDARY = '-'
ZERO_MORPH = '0'
PUNCTUATION = '''“!?,.;"'()«…»'''

def detach_punctuation(token: str) -> tuple[str, str, str]:
    prepuncts = ''
    while len(token) > 0 and token[0] in PUNCTUATION:
        prepuncts += token[0]
        token = token[1:]
    postpuncts = ''
    while len(token) > 0 and token[-1] in PUNCTUATION:
        postpuncts = token[-1] + postpuncts
        token = token[:-1]
    return prepuncts, token, postpuncts

def is_zero_morph(morph: str) -> bool:
    return morph == ZERO_MORPH

def remove_zero_morphs(morphs: Iterable[str]) -> list[str]:
    return list(filterfalse(is_zero_morph, morphs))

def remove_zero_morphs_from_token(token: str) -> str:
    prepuncts, token, postpuncts = detach_punctuation(token)
    morphs = token.split(MORPH_BOUNDARY)
    morphs = remove_zero_morphs(morphs)
    token = MORPH_BOUNDARY.join(morphs)
    token = prepuncts + token + postpuncts
    return token

def unsegment(segmented_word: str) -> str:
    """Removes morpheme boundaries from a segmented word

    :param segmented_word: A word split into morphemes with dashes
    :return: The same word with the dashes removed
    """
    return segmented_word.replace(MORPH_BOUNDARY, '')

def preprocess_token(token: str) -> str:
    return unsegment(remove_zero_morphs_from_token(token))

def is_lat(char: str) -> bool:
    """Determines whether the given character is Latin
    """
    return 'a' <= char <= 'z' or 'A' <= char <= 'Z'

def is_cyr(char: str) -> bool:
    """Determines whether the given character is Cyrillic
    """
    return 'а' <= char <= 'я' or 'А' <= char <= 'Я'
