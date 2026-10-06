import re
whitespace = re.compile(r'\s+')

def collapse_whitespace(translation: str) -> str:
  return whitespace.sub(' ', translation)

def normalise_translation(translation: str) -> str:
  return collapse_whitespace(translation).strip()
