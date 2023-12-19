import os
from distutils import dir_util

import pytest


DATA_DIR = "data"


@pytest.fixture(scope="module")
def datadir(tmpdir_factory, request):
    """
    Fixture responsible for searching a folder with the same name as test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    """
    file_path = request.module.__file__
    test_dir = os.path.splitext(file_path)[0]
    original_data_dir_ = os.path.join(os.path.dirname(test_dir), DATA_DIR)
    dir_name = os.path.basename(test_dir)

    datadir_ = tmpdir_factory.mktemp(dir_name)
    dir_util.copy_tree(original_data_dir_, str(datadir_))

    return datadir_
