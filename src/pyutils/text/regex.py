import re


RE = {
    'url': r'http(?:s)?:\/\/.(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&/=]*)',
    'python_import_libs': r'(from \S{1,})*.*import (\S{1,})',
}


SUBS = {
    'punctuation': r'[,.\"!@#$%^&*(){}?/;`~:<>+=-]',
    'extra_whitespaces': r'(?<=[ ]{1})[ ]{2,}',
    'markdown_headers': r'^[#]{1,}|(?<=\n)[#]{1,}',
}


MARKDOWN = {
    'headers': r'(?<=^[#]{{{level}}} |(?<=\n)[#]{{{level}}} )[^\t\n]+',  # requires level

}


def increase_markdown_header(text):
    regex = re.compile(SUBS['markdown_headers'])

    return regex.sub(lambda m: m.group() + '#', text)


def decrease_markdown_header(text):
    regex = re.compile(SUBS['markdown_headers'])

    return regex.sub(lambda m: m.group()[:-1], text)


def get_markdown_headers(text, level):
    regex = re.compile(MARKDOWN['headers'].format(level=level))

    return regex.findall(text)
