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

    def test_fread_and_fwrite(self):
        filename = osp.join(self.tmpdir, "test.vdk")
        fs.init(filename, 500)
        data = "test_existing_file_with_unicode_éé❤"
        file = fs.fopen("/test", "w")
        file.fwrite(data)
        file.fclose()
        file2 = fs.fopen("/test", "r")
        data2 = file2.fread()
        content = fs.ls("/")
        assert data == data2
