import os
import os.path as osp
import sys
from tempfile import mkdtemp
import random
import shutil

sys.path.insert(
    0, osp.abspath(osp.join(osp.dirname(osp.abspath(__file__)), "..", ".."))
)
from disk import Disk


class TestDiskSeek(object):
    def setup_method(self):
        self.tmpdir = mkdtemp()

    def teardown_method(self):
        shutil.rmtree(self.tmpdir)

    def test_nb_blocks(self):
        for i in range(1, 3):
            filename = osp.join(self.tmpdir, "testseek{}.vdk".format(i))
            block_nr = random.randrange(0, 2047)
            p = Disk(filename)
            p.write(block_nr, "".encode())
            assert p.nb_blocks() == block_nr
