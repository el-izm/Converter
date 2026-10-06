from typing import TypedDict

class TokenDict(TypedDict):
  itoken: str
  tagsets: list[list[str]]
  token: str

class ConstituentDict(TypedDict):
  id: str
  tags: list[str]
  text: str
  tokens: list[list[str]]
