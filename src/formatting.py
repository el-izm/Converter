from translator.conversion.properties.auxiliary import split_feat_val
from translator.conversion.properties.layered_features import format_layered_feature
from unit import Unit

LAYERED_FEATURES = {'Person', 'Number'}
VERB_LAYER = 'word'

def format_subj_feats(unit: Unit) -> list[str]:
  feats = unit.tag
  new_feats = list[str]()
  for feat_val in feats:
    feat, val = split_feat_val(feat_val)
    if feat in LAYERED_FEATURES:
      new_feats.append(format_layered_feature(feat, VERB_LAYER, val))
    else:
      new_feats.append(feat_val)
  return new_feats

def get_formatted_clitic_agr_feats(clitic: Unit, layer: str) -> list[str]:
  clitic_feats = clitic.tag
  clitic_agr_feats = list[str]()
  for feat_val in clitic_feats:
    feat, val = split_feat_val(feat_val)
    if feat in LAYERED_FEATURES:
      new_feat_val = format_layered_feature(feat, layer, val)
      clitic_agr_feats.append(new_feat_val)
    elif feat in ('Reflex', 'Reciprocal'):
        clitic_agr_feats.append(feat_val)
  return clitic_agr_feats