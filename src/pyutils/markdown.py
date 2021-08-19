import re

from pyutils import regex_lib


def increase_header(text):
    regex = re.compile(regex_lib.markdown_headers_symbol())

    return regex.sub(lambda m: m.group() + '#', text)


def decrease_header(text):
    regex = re.compile(regex_lib.markdown_headers_symbol())

    return regex.sub(lambda m: m.group()[:-1], text)


def get_headers(text, level=None):
    regex = re.compile(regex_lib.markdown_header(level=level))

    return regex.findall(text)


def get_leveled_headers():
    # TODO
    pass
