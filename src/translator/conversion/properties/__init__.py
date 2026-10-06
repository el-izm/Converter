from .conversion import convert_properties_to_ud
from .part_of_speech import extract_part_of_speech_from_bundles
from .layered_features import format_bundles
from itertools import chain
from .defaults import add_defaults

def get_feats(properties: list[str], upos: list[str]) -> tuple[list[str], str]:
  """Convert a list of Leipzig-style morphosyntactic property labels
  to a Universal Dependencies-style feature-value mapping
  representing a complete morphosyntactis property set.
  Add the default values necessary to make it complete.
  Change the part of speech if it is specified as a value
  of the POS feature.

  :param properties: A list of morphosyntactic properties.
  :param upos: A list whose first element is the part of speech.
  :return: A tuple consisting of a list of Feature=Value pairs
  and the part of speech.
  """

  part_of_speech = upos[0]

  # Преобразуем каждую глоссу в список соответствующих ей
  # пар признак-значение.
  bundles: list[list[str]] = convert_properties_to_ud(properties)

  # Извлечение части речи из пар признак-значение должно происходить
  # до подстановки [psor], поскольку [psor] релевантно только для существительных, и
  # до подставноки дефолтных значений, поскольку дефолтные значения
  # разные для разных частей речи.
  bundles, part_of_speech = extract_part_of_speech_from_bundles(bundles, part_of_speech)

  # Подстановка [psor]
  bundles = format_bundles(bundles, part_of_speech)

  # Объединим списки пар признак-значение, соответствующие отдельным глоссам, в единый список.
  feats: list[str] = list(chain.from_iterable(bundles))

  # Подстановка дефолтных значений изменяет исходный список и возвращает ссылку на него же.
  feats_with_defaults: list[str] = add_defaults(part_of_speech, feats)

  # Устранение повторяющихся значений.
  # Важно: происходит в последнюю очередь, после подстановки psor и под.
  deduplicated_feats = list[str]()
  for feat in feats_with_defaults:
    if feat not in deduplicated_feats:
      deduplicated_feats.append(feat)

  return deduplicated_feats, part_of_speech
 
