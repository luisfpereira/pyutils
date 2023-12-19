import re

import pytest

from pyutils import regex_lib


def test_url():

    scenarios = [
        "this is a url https://github.com/\n",
        "[joplin style](https://docs.python.org/3/howto/regex.html)",
    ]

    expected_output = [
        "https://github.com/",
        "https://docs.python.org/3/howto/regex.html",
    ]

    text = "".join(scenarios)
    regex = re.compile(regex_lib.url())

    output = regex.findall(text)

    assert output == expected_output


def test_python_imports():

    scenarios = [
        "import fitz\n",
        "from PIL import Image\n",
        "import io\n",
        "import matplotlib.pyplot\n",
        "from  matplotlib   import pyplot  as plt",
    ]

    expected_output = [
        ("", "fitz", ""),
        ("PIL", "Image", ""),
        ("", "io", ""),
        ("", "matplotlib.pyplot", ""),
        ("matplotlib", "pyplot", "plt"),
    ]

    text = "".join(scenarios)
    regex = re.compile(regex_lib.python_import())

    output = regex.findall(text)

    assert output == expected_output


def test_extra_whitespace():

    text = "Too much  white   spaces.\n\tbut keep    breaklines and tabs"
    expected_output = "Too much white spaces.\n\tbut keep breaklines and tabs"

    regex = re.compile(regex_lib.extra_whitespaces())

    output = regex.sub("", text)

    assert output == expected_output


def test_punctuation():
    scenarios = [
        "Removing urls such as (https://github.com/).\n",
        "And $ # % `punctuation`",
    ]

    expected_output = "Removing urls such as \nAnd punctuation"

    text = "".join(scenarios)

    exprs = [regex_lib.url(), regex_lib.punctuation(), regex_lib.extra_whitespaces()]
    subs_regexes = [re.compile(expr) for expr in exprs]

    output = text
    for subs_regex in subs_regexes:
        output = subs_regex.sub("", output)

    assert output == expected_output


def test_markdown_headers_symbol():

    regex = re.compile(regex_lib.markdown_headers_symbol())

    scenarios = ["# This is a header\n", "## this is another, but not # this"]

    expected_output = ["#", "##"]

    text = "".join(scenarios)

    output = regex.findall(text)

    assert output == expected_output
