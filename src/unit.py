class Unit:

  @property
  def tag(self) -> list[str]:
    raise NotImplementedError

  @tag.setter
  def tag(self, value: list[str]) -> None:
    raise NotImplementedError

  @property
  def form(self) -> str:
    raise NotImplementedError

  @form.setter
  def form(self, value: str) -> None:
    raise NotImplementedError

  @property
  def index(self) -> int:
    raise NotImplementedError

  @index.setter
  def index(self, value: int) -> None:
    raise NotImplementedError
