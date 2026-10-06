import re
from re import Pattern

class AttributionRemover:
    pattern: Pattern[str] = re.compile(r"[А-ЯЁ]{2}:|\[[А-ЯЁA-Z]{2}:?\]")

    @classmethod
    def remove_attribution(cls, line: list[str]) -> list[str]:
        if len(line) > 0:
            matching = cls.pattern.fullmatch(line[0])
            if matching is not None:
                return line[1:]
        return line
