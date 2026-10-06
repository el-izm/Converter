import json
from tqdm.auto import tqdm
from ..model.glossing.sentence import GlossedSentence
from ..model.ud.sentence import UDSentence

def convert_glossed_sentences_to_UD_sentences(glossed_sentences: list[GlossedSentence]) -> list[UDSentence]:
    UD_sentences = list[UDSentence]()
    for glossed_sentence in tqdm(glossed_sentences):
        UD_sentence = glossed_sentence.to_UD_sentence()
        UD_sentences.append(UD_sentence)
    return UD_sentences

def conllu_to_file(text: list[UDSentence], name_of_file: str) -> None:
  with open(name_of_file, "w", encoding="utf-8") as fout:
    for sentence in text:
        sentence.print_as_conllu(fout)

def conllu_to_console(text: list[UDSentence]) -> None:
    for sentence in text:
        sentence.print_as_conllu()

def conllu_to_json(UD_sentences: list[UDSentence], name_of_file: str, source: str, url: str) -> None:
  final_list = []
  for sentence in UD_sentences:
    dict_for_sent = sentence.to_dict(source, url)
    final_list.append(dict_for_sent)

  with open(name_of_file, "w", encoding='utf-8') as out_file:
    json.dump(final_list, out_file, indent = 6, ensure_ascii = False)
