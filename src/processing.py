from unit import Unit
from typing import Sequence
from merging import merge_clitic_and_verb, merge_clitic_and_noun, format_verb_object, format_noun_object
from typing import TypeVar, Callable
T = TypeVar('T')

def process_elements[T](elements: list[T], make_unit: Callable[[T], Unit]) -> None:
  i = 0
  while i < len(elements):
    index = i + 1
    unit = make_unit(elements[i])
    if 'VERB' in unit.tag:
      format_verb_object(unit)
      unit.index = index
    elif 'NOUN' in unit.tag:
      format_noun_object(unit)
      unit.index = index
    elif i + 1 < len(elements):
      next_unit = make_unit(elements[i + 1])
      if 'Clitic=Yes' in unit.tag and 'VERB' in next_unit.tag:
        del elements[i]
        merge_clitic_and_verb(unit, next_unit)
        next_unit.index = index
      elif 'Clitic=Yes' in unit.tag and 'NOUN' in next_unit.tag:
        del elements[i]
        merge_clitic_and_noun(unit, next_unit)
        next_unit.index = index
      else:
        unit.index = index
    else:
      unit.index = index
    i += 1
