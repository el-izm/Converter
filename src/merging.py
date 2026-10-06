from formatting import format_subj_feats, get_formatted_clitic_agr_feats
from unit import Unit
from constituent import Constituent

CLITIC_OBJ_LAYER = 'clobj'
CLITIC_PSOR_LAYER = 'clpos'

def merge_clitic_and_verb(clitic: Unit, verb: Unit) -> None:
  clitic_agr_feats = get_formatted_clitic_agr_feats(clitic, CLITIC_OBJ_LAYER)
  verb_feats = format_subj_feats(verb)
  verb.tag = [verb_feats[0]] + clitic_agr_feats + verb_feats[1:]
  verb.form = clitic.form + verb.form
  if 'segmentation' in clitic.dict:
    verb.dict['segmentation'] = clitic.dict['segmentation'] + "-" + verb.dict['segmentation']
    verb.dict['gloss'] = clitic.dict['gloss'] + "-" + verb.dict['gloss']
  if isinstance(clitic, Constituent) and isinstance(verb, Constituent):
    verb.token_form = clitic.token_form + verb.token_form

def merge_clitic_and_noun(clitic: Unit, noun: Unit) -> None:
  clitic_psor_feats = get_formatted_clitic_agr_feats(clitic, CLITIC_PSOR_LAYER)
  noun_feats = format_subj_feats(noun)
  upos = noun_feats[0]
  noun.tag = [upos] + noun_feats[1:] + clitic_psor_feats
  noun.form = clitic.form + noun.form
  if 'segmentation' in clitic.dict:
    noun.dict['segmentation'] = clitic.dict['segmentation'] + "-" + noun.dict['segmentation']
    noun.dict['gloss'] = clitic.dict['gloss'] + "-" + noun.dict['gloss']
  if isinstance(clitic, Constituent) and isinstance(noun, Constituent):
    noun.token_form = clitic.token_form + noun.token_form

def format_verb_object(verb: Unit) -> None:
  verb.tag = format_subj_feats(verb)

def format_noun_object(noun: Unit) -> None:
  noun.tag = format_subj_feats(noun)
