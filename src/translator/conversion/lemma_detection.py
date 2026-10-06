import re

def lemmas_gram(segmentation: str, gloss: str) -> tuple[list[str], list[list[str]]]:

    # Функция принимает на вход нивхскую словоформу и соответствующую ей глоссу
    # и возвращает две леммы (нивхскую и русскую) и список грамматических признаков,
    # которые извлекаются из русской глоссы.

    #print(token1)
    if segmentation and gloss:
      segmentation = segmentation.strip("?")
      token1 = segmentation.split("-")   # разбиваем входные токены по дефисам
      match1 = re.search(r"\w+-(нибудь|то|либо|таки)\b|еле-еле|чуть-чуть|едва-едва|кое-\w+", gloss)  # Поправить "то"! Сейчас, видимо, отлавливаются слова типа "это-тоже" и др.
      if match1:
        start = match1.start()
        end = match1.end()
        gloss = gloss[:start] + gloss[0].replace("-", "~") + gloss[end:]
      token2 = gloss.split("-")

      pairs = list[tuple[str, str]]()
      #print(token1)
      for index in range(0, len(token2)):
        key = token1[index]
        value = token2[index]
        pairs.append((key, value))   # складываем соотнесенные морфемы и глоссы в словарь

      lemmas = []
      gram = []

      for key, value in pairs:
          if any('а' <= char <= 'я' or 'А' <= char <= 'Я' for char in value):
              #lemmas[key] = value   # если в глоссах слово на кириллице, значит оно само и соответствующая нивхская часть - леммы
              lemmas.extend([key, value])                   # нивхская лемма должна записываться в 'lemma', русская - идти на вход русскому морфологическому анализатору, чтобы определить чр
          else:
              gram.append(re.split(r'[.:]', value))   # все из глосс, что не леммы, мы собираем в общий список, который потом отправится в функцию get_feats() на переработку в формат ConLLU

      if lemmas:
        if any('a' <= char <= 'z' or 'A' <= char <= 'Z' for char in lemmas[1]):
          # print(str(lemmas[1]) + "\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
          temp_list = lemmas[1].split(".")
          #print(temp_list)
          for x in temp_list:
            if not any('а' <= char <= 'я' or 'А' <= char <= 'Я' for char in x):
              gram.append([x])
              #print(x)
              lemmas[1] = lemmas[1].replace(x, "")
        lemmas[1] = lemmas[1].strip(".")
        lemmas[1] = lemmas[1].strip("?") #убираем ? из русской леммы
        #print(lemmas[1])

      return lemmas, gram
    else:
      return ["NaN", "NaN"], [["NaN"], ["NaN"]]
