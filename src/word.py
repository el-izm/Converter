from unit import Unit
from type_definition import TokenDict

class Token(Unit):

  def __init__(self, dict: TokenDict):
    self.dict = dict

  @property
  def tag(self) -> list[str]:
    return self.dict['tagsets'][0]

  @tag.setter
  def tag(self, value: list[str]) -> None:
    self.dict['tagsets'][0] = value

  @property
  def form(self) -> str:
    return self.dict['token']

  @form.setter
  def form(self, value: str) -> None:
    self.dict['token'] = value

  @property
  def index(self) -> int:
    return int(self.dict['itoken'])

  @index.setter
  def index(self, value: int) -> None:
    self.dict['itoken'] = str(value)
