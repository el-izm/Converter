from .auxiliary import split_feat_val, split_feat_vals

POSSESSOR_ATTRIBUTE_MARKER = 'clpos'
LAYER_FEATURE_NAME = 'Layer'

def contains_a_value_for(bundle: list[str], feature: str) -> bool:
  """Determine whether a given bundle of Feature=Value strings
  contains a value for the specified Universal Dependencies morphological feature.

  :param bundle: A bundle of Feature=Value string.
  :param feature: A Universal Dependencies morphological feature, such as Person.
  :return: True if the bundle contains a value of the specified feature, False otherwise.
  """
  for feat, val in split_feat_vals(bundle):
    if feat == feature:
      return True
  return False

def get_value_for(bundle: list[str], feature: str) -> str | None:
  """Return a value for the specified Universal Dependencies morphological feature
  from the given given bundle of Feature=Value strings.

  :param bundle: A bundle of Feature=Value string.
  :param feature: A Universal Dependencies morphological feature, such as Person.
  :return: A value if the bundle contains the specified feature, None otherwise.
  """
  for feat, val in split_feat_vals(bundle):
    if feat == feature:
      return val
  return None

def exists_and_contains_a_value_for(bundles: list[list[str]], position: int, feature: str) -> bool:
  """For the specified position, determine whether the position
  is for valid the provided list of Feature=Value string bundles
  and the bundle in this position contains a value
  for the specified Universal Dependencies morphological feature.

  :param bundles: A list of Feature=Value string bundles.
  :param position: The index of the element which should be considered.
  :param feature: A Universal Dependencies morphological feature, such as Person.
  :return: True if the position is well-defined (0 <= position < len(feats))
  and the bundle in this position contains a value
  for the specified feature; False otherwise.
  """
  if position >= 0 and position < len(bundles):
    bundle = bundles[position]
    return contains_a_value_for(bundle, feature)
  else:
    return False

def get_layer(part_of_speech: str, feat: str, bundles: list[list[str]], position: int) -> str | None:
  """For a feature occuring at the specified position in a list of
  Feature=Value string bundles, determine whether
  the feature is a layered feature and what the appropriate layer is.

  :param part_of_speech: The part of speech of the word form under consideration.
  :param feat: A possibly layered Universal Dependencies morphological feature.
  :param bundles: A list of morphosyntactic properties.
  :param position: The index of the morphosyntactic property for which the layer should be determined, if needed.
  :return: A layer if the feature is layered and the layer should be marked, None otherwise.
  """
  if feat == 'Person' or feat == 'Number':
    match part_of_speech:
      case 'NOUN':
        for search_position in range(position - 1, position + 1):
          if exists_and_contains_a_value_for(bundles, search_position, 'Person'):
            return POSSESSOR_ATTRIBUTE_MARKER
      case 'VERB':
        for search_position in range(position, position + 3):
          if exists_and_contains_a_value_for(bundles, search_position, LAYER_FEATURE_NAME):
            bundle = bundles[search_position]
            return get_value_for(bundle, LAYER_FEATURE_NAME)
      case _:
        pass
  return None

def format_layered_feature(feat: str, layer: str, val: str) -> str:
  """Provide a string representation of the form Feature[layer]=Value
  (as required by the Universal Dependencies documentation)
  for a given layered feature, layer and value.

  :param feat: A layered Universal Dependencies morphological feature, e. g. Number.
  :param layer: A layer, e. g. psor, psee, erg, dat
  :param value: A value for the given feature in the specified layer.
  :return: A string representation following the Feature[layer]=Value template.
  """
  return '{0}[{1}]={2}'.format(feat, layer, val)

def format_feature(feat_val: str, part_of_speech: str, bundles: list[list[str]], position: int) -> str:
  """Determine if the feature is layered and provide a string
  representation of the form Feature=Value or Feature[layer]=Value
  for a given feature and value occuring in a bundle of features
  at the specified position in the morphological property list of word form
  with the given part of speech.

  :param feat: A layered Universal Dependencies morphological feature, e. g. Number.
  :param value: A value for the given feature in the specified layer.
  :param part_of_speech: The part of speech of the word form under consideration.
  :param feats: A list of morphosyntactic properties.
  :param position: The index of the morphosyntactic property for which the layer should be determined, if needed.
  :return: A string representation following the Feature=Value template.
  """
  feat, val = split_feat_val(feat_val)
  layer = get_layer(part_of_speech, feat, bundles, position)
  if layer is not None:
    return format_layered_feature(feat, layer, val)
  else:
    return feat_val

def format_bundle(bundle: list[str], part_of_speech: str, bundles: list[list[str]], position: int) -> list[str]:
  """For each feature in the given bundle occurring at the specified position
  in the morphological property list of a word form with the given part of speech,
  determine if the feature is layered and provide a string
  representation of the form Feature=Value or Feature[layer]=Value.

  :param bundle: A bundle of Feature=Value strings.
  :param part_of_speech: The part of speech of the word form under consideration.
  :param feats: A list of morphosyntactic properties.
  :param position: The index of the morphosyntactic property for which the layer should be determined, if needed.
  :return: A list of morphosyntactic property representations
  following the template Feature=Value or Feature[layer]=Value, as appropriate.
  """
  new_bundle = list[str]()
  for feat_val in bundle:
    feat_val = format_feature(feat_val, part_of_speech, bundles, position)
    new_bundle.append(feat_val)
  return new_bundle

def format_bundles(bundles: list[list[str]], part_of_speech: str) -> list[list[str]]:
  """For each feature in each bundle of Feature=Value strings
  in the morphological property list of a word form with the given part of speech,
  determine if the feature is layered and provide a string
  representation of the form Feature=Value or Feature[layer]=Value.
  """
  new_bundles = list[list[str]]()
  for position, bundle in enumerate(bundles):
    new_bundle = format_bundle(bundle, part_of_speech, bundles, position)
    filtered_bundle = list(filter(lambda feat_val: split_feat_val(feat_val)[0] != LAYER_FEATURE_NAME, new_bundle))
    if len(filtered_bundle) > 0:
      new_bundles.append(new_bundle)
  return new_bundles
