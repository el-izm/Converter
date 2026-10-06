class TokenFilter:
  tokens_to_remove = {'—', ','}

  @classmethod
  def filter_tokens(cls, tokens: list[str]) -> list[str]:
    return list(filter(lambda token: token not in cls.tokens_to_remove, tokens))
