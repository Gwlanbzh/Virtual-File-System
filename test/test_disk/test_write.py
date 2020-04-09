import os
import os.path as osp
import shutil
import sys

from tempfile import mkdtemp

import pytest

sys.path.insert(
    0, osp.abspath(osp.join(osp.dirname(osp.abspath(__file__)), "..", ".."))
)
from disk import Disk


class TestDiskConstructor(object):
    def setup_method(self):
        self.tmpdir = mkdtemp()

    def teardown_method(self):
        shutil.rmtree(self.tmpdir)

    def test_should_write_unicode(self):
        filename = osp.join(self.tmpdir, "test.vdk")
        initial_content = "test_existing_file_with_unicode_éé❤"
        p = Disk(filename)
        p.write(1, initial_content.encode())
        with open(filename, "rb") as f:
            data = f.read().decode()
            data = data.replace("\x00", "")
        assert len(initial_content) == len(data)
        assert initial_content == data
