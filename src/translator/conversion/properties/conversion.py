from ...atr_val import morphdict
from .auxiliary import split_bundle
from warnings import warn
from logging import getLogger
logger = getLogger(__name__)

def convert_properties_to_ud(feats: list[str]) -> list[list[str]]:
  """Convert a list of morphosyntactis property labels
  to a list of bundles of Feature=Value pairs.

  :param feats: A list of morphosyntactic properties.
  :return: A list of bundles of Feature=Value pairs.
  """
  bundles = list[list[str]]()
  for position, gloss in enumerate(feats):
    if gloss not in morphdict:
      warn(f'The morphosyntactic property {gloss} is missing from atr_val.py')
      logger.warning('The morphosyntactic property %s is missing from atr_val.py', gloss)
    else:
      feat_vals = morphdict[gloss]
      bundle = split_bundle(feat_vals)
      bundles.append(bundle)
  return bundles
