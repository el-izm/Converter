from .atr_val import adjectives as language_has_adjectives

import stanza
stanza_model = stanza.Pipeline('ru', processors='tokenize,pos,lemma,depparse')

memory = dict[str, list[str]]()

PROPER_NOUNS = {"нивх", "айн"}

def define_pos_tag(lemma: str) -> list[str]:

  if lemma in memory:
    return memory[lemma]

  # Функция принимает на вход русскую лемму, прогоняет её через Станзу
  # и возвращает одноэлементный список с одной строкой - часть речи леммы.

  splitted_lemma = " ".join(lemma.split("."))

  if "~" in splitted_lemma:
    splitted_lemma = splitted_lemma.replace("~", "-")

  if splitted_lemma == "сам":
    return ["PRON"]

  analysis = stanza_model(splitted_lemma)     # Сюда можно добавить условие, что если в splitted_lemma одно слово, то не надо проверять его на word.deprel == root. М.б. из-за этого получается долго
  upos_tag1 = [f'{word.upos}' for snt in analysis.sentences for word in snt.words if word.deprel == "root"]
  if not language_has_adjectives and upos_tag1[0] == "ADJ":
    upos_tag1 = ["VERB"]
  if 'быть ' in splitted_lemma:
    upos_tag1 = ["VERB"]
  if splitted_lemma in PROPER_NOUNS or splitted_lemma[0].isupper():
      return ["NOUN"]
  memory[lemma] = upos_tag1
  return upos_tag1
