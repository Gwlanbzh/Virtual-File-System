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

    def test_should_place_cursor_at_beginning(self):
        filename = osp.join(self.tmpdir, "test.vdk")
        p = Disk(filename)
        assert p.cursor == 0

    def test_should_open_and_read_existing_file(self):
        filename = osp.join(self.tmpdir, "test.vdk")
        initial_content = "test_existing_file_with_unicode_éé❤"
        with open(filename, "wb") as f:
            data = initial_content.encode()
            data += b"\x00" * (3 * 512 - len(data))
            f.write(data)
        p = Disk(filename)
        content = p.read(3)
        assert len(content) == len(data)
        assert content == data
