import re

import pytest

# TODO: delete

from pyutils import regex_lib
from pyutils.markdown import increase_header
from pyutils.markdown import decrease_header
from pyutils.markdown import get_headers


def test_markdown_level():

    scenarios = ['# This is a header\n',
                 '## this is another, but not # this']

    text = ''.join(scenarios)

    # increase level
    expected_output = '## This is a header\n### this is another, but not # this'
    output = increase_header(text)
    assert output == expected_output

    # decrease level
    expected_output = 'This is a header\n# this is another, but not # this'
    output = decrease_header(text).lstrip()
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
        output = get_headers(text, i + 1)

        assert output == expected_output
