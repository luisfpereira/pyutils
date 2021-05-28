'''Library of regex expressions. I've chosen to represent them as functions to
make use of docstrings, otherwise they become unusable really fast (as they
are unintelligible immediately after I develop them).

Notes
-----
* function names, exceptionally, do not follow good practice of starting by a
verb.
'''


def url():
    return r'http(?:s)?:\/\/.(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&/=]*)'


def python_imports():
    '''Returns python import in groups, considering the general statement
    `from <g1> import <g2> as <g3>`
    '''
    # TODO: deal with multiple imports from the same place
    return r'(?:from[ ]+)*(\S{1,})*[ ]*import[ ]+(\S{1,})(?:[ ]+as[ ]+)*(\S{1,})*'


def punctuation(chars=',.\"!@#$%^&*(){}?/;`~:<>+=-'):
    '''Finds characters in text. Useful to preprocess text. Do not forget
    to escape special characters.
    '''
    return rf'[{chars}]'


def extra_whitespaces():
    '''Specially useful to remove extra whitespaces from text. Just replace
    by an empty str.
    '''
    return r'(?<=[ ]{1})[ ]{1,}'


def markdown_headers_symbol():
    '''Get markdown headers symbol (to get or change level).
    '''
    return r'^[#]{1,}|(?<=\n)[#]{1,}'


def markdown_headers(level):
    '''Get markdown headers (without symbol).
    '''
    return rf'(?<=^[#]{{{level}}} |(?<=\n)[#]{{{level}}} )[^\t\n]+'
