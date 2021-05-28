import re

import pytest

# TODO: delete

from pyutils.text import regex_lib
from pyutils.text.regex import increase_markdown_header
from pyutils.text.regex import decrease_markdown_header
from pyutils.text.regex import get_markdown_headers


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
