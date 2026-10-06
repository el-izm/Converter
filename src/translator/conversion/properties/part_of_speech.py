from .auxiliary import split_feat_val, PART_OF_SPEECH_FEATURE_NAME
from logging import getLogger
logger = getLogger(__name__)

def extract_part_of_speech_from_bundle(bundle: list[str]) -> tuple[list[str], str | None]:
  """For a given list of Feature=Value pairs and a part of speech,
  check if any feature is the part of speech feature (POS) and extract
  it from the list if found, setting the part of speech to the provided value.

  :param bundle: A list of Universal Dependencies-style Feature=Value pairs
  representing morphosyntactic properties and possibly the part of speech (POS).
  :return: A tuple consisting of
  (1) a list of Feature=Value pairs representing morphosyntactic properties
  (2) the part of speech if present, None otherwise.
  """
  new_bundle = list[str]()
  part_of_speech = None
  for feat_val in bundle:
    feat, val = split_feat_val(feat_val)
    if feat == PART_OF_SPEECH_FEATURE_NAME:
      part_of_speech = val.upper()
    else:
      new_bundle.append(feat_val)
  return new_bundle, part_of_speech

def extract_part_of_speech_from_bundles(bundles: list[list[str]], original_part_of_speech: str) -> tuple[list[list[str]], str]:
  """For a given list of bundles of Feature=Value pairs and a part of speech,
  check if any feature in any bundle is the part of speech feature (POS) and extract
  it from that bundle if found, setting the part of speech to the provided value.
  Return the original part of speech if no part of speech attribute was found.
  If multiple bundles containt a value for the part of speech feature,
  return the last value and log the override event.

  :param bundle: A list of bundles of Universal Dependencies-style Feature=Value pairs
  representing morphosyntactic properties and possibly the part of speech (POS).
  :param upos: The original part of speech, which should be overridden by the POS
  attribute if present.
  :return: A tuple consisting of as list of bundles Feature=Value pairs representing
  morphosyntactic properties and the part of speech (either original or
  from the POS attribute, if present).
  """
  new_bundles = list[list[str]]()
  part_of_speech = None
  for bundle in bundles:
    new_bundle, new_part_of_speech = extract_part_of_speech_from_bundle(bundle)
    if len(new_bundle) > 0:
      new_bundles.append(new_bundle)
    if new_part_of_speech is not None:
      if part_of_speech is not None:
        logger.warning('The part of speech %s has been overridden with %s.',
                       part_of_speech, new_part_of_speech)
      part_of_speech = new_part_of_speech
  if part_of_speech is None:
    part_of_speech = original_part_of_speech
  return new_bundles, part_of_speech
