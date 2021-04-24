
import os

import pytest
import pyclip

from pyutils.clipboard import XclipCommand


def test_xclip_png(datadir):

    image_name = os.path.join(datadir, 'example.png')

    cmd = XclipCommand()

    # clear clipboard
    pyclip.clear()

    # check if run was successful
    assert os.system(cmd.get_cmd(image_name)) == 0

    # check if clipboard was filled
    txt = pyclip.paste()

    assert txt != ""
