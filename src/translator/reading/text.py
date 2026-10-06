from ..model.glossing.sentence import GlossedSentence
from .sentence import SentenceParser

def read_sentences_from_file(filename: str, skipped_sentences_filename: str) -> list[GlossedSentence]:
    """Reads a glossed text from a file and converts it to a list of sentences.

    :param filename: The name of the file to read the glossed text from
    :return: A list of sentences with linguistic annotations from the specified file
    """
    sentences: list[GlossedSentence] = list[GlossedSentence]()
    parser = SentenceParser()

    with open(filename, "r", encoding="utf-8-sig") as fin, open(skipped_sentences_filename, 'w', encoding='utf-8') as log:
        while True:
            sentence = parser.read_sentence_from_stream(fin)
            if sentence is None:
                break
            if sentence.raw.has_formatting_issue:
                print(sentence.raw.glossed_text, file=log)
            else:
                sentences.append(sentence)
    return sentences
