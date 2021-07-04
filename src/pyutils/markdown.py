import re

from pyutils.regex_lib import regex_lib


def increase_markdown_header(text):
    regex = re.compile(regex_lib.markdown_headers_symbol())

    return regex.sub(lambda m: m.group() + '#', text)


def decrease_markdown_header(text):
    regex = re.compile(regex_lib.markdown_headers_symbol())

    return regex.sub(lambda m: m.group()[:-1], text)


def get_markdown_headers(text, level):
    regex = re.compile(regex_lib.markdown_headers(level=level))

    return regex.findall(text)
