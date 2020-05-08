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

    def test_ls_empty_dir(self):
        filename = osp.join(self.tmpdir, "test.vdk")
        fs.init(filename, 500)
        content = fs.ls("/")
        assert content == []

    def test_ls_with_dir(self):
        filename = osp.join(self.tmpdir, "test.vdk")
        fs.init(filename, 500)
        fs.mkdir("/", "dir1")
        fs.mkdir("/", "dir2")
        content = fs.ls("/")
        print(content)
        assert content == [[b"dir1", [6], b"0"], [b"dir2", [7], b"0"]]

    def test_ls_with_files(self):
        filename = osp.join(self.tmpdir, "test.vdk")
        fs.init(filename, 500)
        file1 = fs.fopen("/file1", "w")
        file1.fwrite("test")
        file1 = fs.fopen("/file2", "w")
        file1.fwrite("test")
        content = fs.ls("/")
        print(content)
        assert content == [[b"file1", [6], b"1"], [b"file2", [7], b"1"]]
