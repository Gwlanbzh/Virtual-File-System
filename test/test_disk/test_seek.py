import os
import os.path as osp
import random
import shutil
import sys

from tempfile import mkdtemp

sys.path.insert(
    0, osp.abspath(osp.join(osp.dirname(osp.abspath(__file__)), "..", ".."))
)
from disk import Disk


class TestDiskSeek(object):
    def setup_method(self):
        self.tmpdir = mkdtemp()
        self.filename = osp.join(self.tmpdir, "testseek.vdk")
        self.p = Disk(self.filename)
        self.p.write(2048, "".encode())

    def teardown_method(self):
        shutil.rmtree(self.tmpdir)

    def test_seek_file_size(self):
        file_stats = os.stat(self.filename)
        # Check we have created a file with 2048 blocks of 512 bytes
        assert file_stats.st_size == (2048 * 512)

    def test_seek_beginning(self):
        self.p.seek(0)
        assert self.p.cursor == 0

    def test_seek_end(self):
        self.p.seek(-1)
        assert self.p.cursor == 2048

    def test_seek_random(self):
        for _ in range(1, 3):
            block_addr = random.randrange(0, 2047)
            self.p.seek(block_addr)
            assert self.p.cursor == block_addr

    def test_seek_outside_bound(self):
        exception_raised = False
        assert self.p.seek(5120) == -1
