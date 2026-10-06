from unit import Unit
from type_definition import ConstituentDict

class Constituent(Unit):

  def __init__(self, dict: ConstituentDict):
    self.dict = dict

  @property
  def tag(self) -> list[str]:
    return self.dict['tags']

  @tag.setter
  def tag(self, value: list[str]) -> None:
    self.dict['tags'] = value

  @property
  def form(self) -> str:
    return self.dict['text']

  @form.setter
  def form(self, value: str) -> None:
    self.dict['text'] = value

  @property
  def token_form(self) -> str:
    return self.dict['tokens'][0][0]

  @token_form.setter
  def token_form(self, value: str) -> None:
    self.dict['tokens'][0][0] = value

  @property
  def index(self) -> int:
    return int(self.dict['id'])

  @index.setter
  def index(self, value: int) -> None:
    self.dict['id'] = str(value)
