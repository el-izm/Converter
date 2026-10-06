import warnings
from collections.abc import Iterable
from ... import MORPHOSYNTACTIC_PROPERTY_SEPARATOR

FEATURE_VALUE_SEPARATOR = '='
PART_OF_SPEECH_FEATURE_NAME = 'POS'

def split_feat_val(feat_val: str) -> tuple[str, str]:
  """Split a Feature=Value pair into Feature and Value.

  :param feat_val: A string of the form Feature=Value.
  :return: A (Feature, Value) tuple.
  """
  split = feat_val.split(FEATURE_VALUE_SEPARATOR, maxsplit=1)
  if len(split) == 2:
    feat, val = split
    return feat, val
  else:
    warnings.warn(f'The feature {feat_val} will be treated as a part of speech tag.')
    return 'POS', feat_val

def split_bundle(bundle: str) -> list[str]:
  """Split a vertical bar-separated bundle of Feature=Value strings
  into a the separate Feature=Value strings.

  :param bundle: A string of the form Feature1=Value1|Feature2=Value2|...
  :return: A list of Feature=Value strings.
  """
  return bundle.split(MORPHOSYNTACTIC_PROPERTY_SEPARATOR)

def split_feat_vals(bundle: Iterable[str]) -> Iterable[tuple[str, str]]:
  """Split each Feature=Value string in a bundle
  into a of (Feature, Value) pair.

  :param bundle: An iterable of Feature=Value strings.
  :return: A iterable of (Feature, Value) tuples.
  """
  return map(split_feat_val, bundle)

def format_simple_feature(feat: str, val: str) -> str:
  """Provide a string representation of the form Feature=Value
  (as required by the Universal Dependencies documentation)
  for a given feature and value, where the feature is not layered.

  :param feat: A layered Universal Dependencies morphological feature, e. g. Number.
  :param value: A value for the given feature in the specified layer.
  :return: A string representation following the Feature=Value template.
  """
  return '{0}={1}'.format(feat, val)

