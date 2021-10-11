import random
from typing import Optional


def wrong_key_typos(query: str, typos: list, keyboard: dict):
    # print(query) #!DEBUG
    query_list = query.split()
    # print(query_list) #!DEBUG
    keyword = query_list[0].lower()
    # print(keyword) #!DEBUG

    for keyword_letter in keyword[1:]:
        if keyword_letter in keyboard.keys():
            modified_keyword = "".join(
                [
                    letter
                    if letter != keyword_letter
                    else keyboard[keyword_letter][
                        random.randint(0, len(keyboard[keyword_letter]) - 1)
                    ]
                    for letter in keyword
                ]
            )

        # print(modified_keyword) #!DEBUG
        modified_query = " ".join([modified_keyword, *query_list[1:]])
        # print(*query_list[1:]) #!DEBUG
        # print(modified_query) #!DEBUG

        typos.append(modified_query)


def missing_chars(query: str, typos: list):
    query_list = query.split()
    keyword = query_list[0].lower()

    for keyword_letter in keyword:
        modified_keyword = keyword.replace(keyword_letter, "")

        modified_query = " ".join([modified_keyword, *query_list[1:]])

        typos.append(modified_query)


def double_char(query: str, typos: list):
    query_list = query.split()
    keyword = query_list[0].lower()

    for keyword_letter in keyword:
        modified_keyword = keyword.replace(keyword_letter, f"{keyword_letter*2}")

        modified_query = " ".join([modified_keyword, *query_list[1:]])

        typos.append(modified_query)


def typoing(query: Optional[str]) -> list:
    if not query:
        return None

    typos = list()
    keyboard = {
        "q": ["w", "a"],
        "w": ["q", "a", "s"],
        "e": ["w", "s", "d"],
        "r": ["e", "d", "f"],
        "t": ["r", "f", "g"],
        "y": ["t", "g", "h"],
        "u": ["y", "h", "j"],
        "i": ["u", "j", "k"],
        "o": ["i", "k", "l"],
        "p": ["o", "l", "-"],
        "a": ["z", "s", "w"],
        "s": ["a", "z", "x"],
        "d": ["s", "x", "c"],
        "f": ["d", "c", "v"],
        "g": ["f", "v", "b"],
        "h": ["g", "b", "n"],
        "j": ["h", "n", "m"],
        "k": ["j", "m", "l"],
        "l": ["k", "p", "o"],
        "z": ["x", "s", "a"],
        "x": ["z", "c", "d"],
        "c": ["x", "v", "f"],
        "v": ["c", "b", "g"],
        "b": ["v", "n", "h"],
        "n": ["b", "m", "j"],
        "m": ["n", "k", "j"],
    }

    missing_chars(query, typos)
    double_char(query, typos)
    wrong_key_typos(query, typos, keyboard)

    return f"({','.join(typos[:20])})" if len(typos) > 1 else None


# print(typoing("playstation 4 controller"))  #!DEBUG
