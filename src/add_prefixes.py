from os import path
import os
import json
from word import Token
from constituent import Constituent
from processing import process_elements

input_directory = 'output'
assert path.exists(input_directory)
output_directory = 'prefixed'
os.makedirs(output_directory, exist_ok=True)

texts_stats = []

for file_name in os.listdir(input_directory):
  short_name, ext = path.splitext(file_name)
  if ext == '.json' and file_name != 'corpus_stats.json':
    print(file_name)
    with open(path.join(input_directory, file_name), 'r', encoding='utf-8') as fin:
      text = json.load(fin)
      for sentence in text:
        process_elements(sentence['tokens'], Token)
        process_elements(sentence['constituents'], Constituent)
        # sentence['length'] = len(sentence['tokens'])
    with open(path.join(output_directory, file_name), 'w', encoding='utf-8') as fout:
      json.dump(text, fout, ensure_ascii=False, indent=6)
    texts_stats.append({
          'file': short_name,
          'num_sentences': len(text),
          'num_tokens': sum(sent['length'] for sent in text),
          **text[0]['metadata']
      })

corpus_stats = {
    'total_sentences': sum(t['num_sentences'] for t in texts_stats),
    'total_tokens': sum(t['num_tokens'] for t in texts_stats),
    'texts': texts_stats
}
with open(path.join(output_directory, 'corpus_stats.json'), 'w', encoding='utf-8') as f:
    json.dump(corpus_stats, f, indent=2, ensure_ascii=False)