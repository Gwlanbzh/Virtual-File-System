import os
import os.path as osp
import random
import shutil
import sys
from math import ceil

from tempfile import mkdtemp

import pytest

sys.path.insert(
    0, osp.abspath(osp.join(osp.dirname(osp.abspath(__file__)), "..", ".."))
)
from disk import Disk
import fs


class TestFsInit(object):
    def setup_method(self):
        self.tmpdir = mkdtemp()

    def teardown_method(self):
        shutil.rmtree(self.tmpdir)

    def test_should_init_fs(self):
        filename = osp.join(self.tmpdir, "test.vdk")
        fs.init(filename, 500)
        file = open(filename, "rb")
        data = file.read()
        assert data[2:3] == b"\xf8"
        assert data[0:2] == b"\x00\x01"
        os.remove(filename)

    def test_should_init_fs_random(self):
        filename = osp.join(self.tmpdir, "test.vdk")
        for _ in range(1, 3):
            taille = random.randrange(0, 65535)
            fs.init(filename, taille)
            file = open(filename, "rb")
            data = file.read()
            table_size = int(ceil(taille / (512 * 8)))
            assert data[2:3] == b"\xf8"
            assert data[0:2] == bytes([table_size // 256, table_size % 256])
            file_stats = os.stat(filename)
            assert file_stats.st_size == taille*512
            os.remove(filename)
