import re

import pytest

from pyutils.text.regex import RE
from pyutils.text.regex import SUBS
from pyutils.text.regex import increase_markdown_header
from pyutils.text.regex import decrease_markdown_header
from pyutils.text.regex import get_markdown_headers


def test_url():

    scenarios = ['this is a url https://github.com/\n',
                 '[joplin style](https://docs.python.org/3/howto/regex.html)']

    expected_output = ['https://github.com/',
                       'https://docs.python.org/3/howto/regex.html']

    text = ''.join(scenarios)
    regex = re.compile(RE['url'])

    output = regex.findall(text)

    assert output == expected_output


def test_python_import_libs():

    scenarios = ['import fitz\n',
                 'from PIL import Image\n',
                 'import io\n',
                 'import matplotlib.pyplot']

    expected_output = [('', 'fitz'),
                       ('from PIL', 'Image'),
                       ('', 'io'),
                       ('', 'matplotlib.pyplot')]

    text = ''.join(scenarios)
    regex = re.compile(RE['python_import_libs'])

    output = regex.findall(text)

    assert output == expected_output


def test_extra_whitespace():

    text = 'Too much  white   spaces.\n\tbut keep    breaklines and tabs'
    expected_output = 'Too much white spaces.\n\tbut keep breaklines and tabs'

    regex = re.compile(SUBS['extra_whitespaces'])

    output = regex.sub('', text)

    assert output == expected_output


def test_punctuation():
    scenarios = ['Removing urls such as (https://github.com/).\n',
                 'And $ # % `punctuation`']

    expected_output = 'Removing urls such as \nAnd punctuation'

    text = ''.join(scenarios)

    expr = RE.copy()
    expr.update(SUBS)
    subs_regexes = [re.compile(expr[key]) for key in ['url', 'punctuation',
                                                      'extra_whitespaces']]

    output = text
    for subs_regex in subs_regexes:
        output = subs_regex.sub('', output)

    assert output == expected_output


def test_markdown_headers():

    regex = re.compile(SUBS['markdown_headers'])

    scenarios = ['# This is a header\n',
                 '## this is another, but not # this']

    expected_output = ['#', '##']

    text = ''.join(scenarios)

    output = regex.findall(text)

    assert output == expected_output


def test_markdown_level():

    scenarios = ['# This is a header\n',
                 '## this is another, but not # this']

    text = ''.join(scenarios)

    # increase level
    expected_output = '## This is a header\n### this is another, but not # this'
    output = increase_markdown_header(text)
    assert output == expected_output

    # decrease level
    expected_output = 'This is a header\n# this is another, but not # this'
    output = decrease_markdown_header(text).lstrip()
    assert output == expected_output


def test_markdown_headers():
    scenarios = ['# This is a header\n',
                 '# This is the second one\n',
                 '## this is another, but not # this']

    text = ''.join(scenarios)

    # level
    expected_outputs = [['This is a header', 'This is the second one'],
                        ['this is another, but not # this']]

    for i, expected_output in enumerate(expected_outputs):
        output = get_markdown_headers(text, i + 1)

        assert output == expected_output
