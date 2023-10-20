import re

from utils.rounding_func import round_dec


def bi_check_type(string: str) -> float:
    string = string.replace(' ', '')
    elements = re.findall(r'\d+\.\d+|\d+', string)
    bi = round_dec(sum(float(elem) for elem in elements))

    return bi
