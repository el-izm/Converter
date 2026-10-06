from ...atr_val import defaults
from .auxiliary import split_feat_val

def meets_conditions(morphs: list[str], conditions: list[str]) -> bool:
  """Determines whether a list of Feature=Value pairs morphs meets given the list of conditions.
  :param morphs: A list of Feature=Value strings.
  :param default: A list of Feature=Value or Feature!=Value strings.
  :return: True if all the conditions are satisfied, False otherwise.
  """
  for condition in conditions:
    if '!=' in condition:
      # Negative condition
      if condition.replace('!=', '=') in morphs:
        # If the negative condition occurs in morphs, it is not satisfied.
        return False
    else:
      # Positive condition
      if not condition in morphs:
        # If the positive condition does not occur in the morphs, it is not satisfied.
        return False
  return True

def add_defaults(part_of_speech: str, morphs: list[str]) -> list[str]:
  """Add default values for morphological features
  which are missing from a given list of Universal Dependencies
  morphological features but required for the given part of speech.

  :param part_of_speech: The part of speech of the word form under consideration.
  :param morphs: A list of Feature=Value pairs representing a Universal Dependencies
  morphosyntactic property set, possibly incomplete.
  :return: The same list of Feature=Value pairs, possibly to with added morphological features,
  now representing a complete morphosyntactic property set.
  """
  if part_of_speech in defaults:
    for default in defaults[part_of_speech]:
      if isinstance(default, tuple):
        conditions, default_feat_val = default
        if not meets_conditions(morphs, conditions):
          continue
      else:
        default_feat_val = default
      feature, value = split_feat_val(default_feat_val)
      if not any(feature == split_feat_val(feature_value_pair)[0] for feature_value_pair in morphs):
        morphs.append(default_feat_val)
  return morphs
