#!/usr/bin/env python3
import raid
from disk import Disk


class Cache(object):
    def __init__(self, name: str, type=""):
        if type == "":
            self.disk = Disk(name)
        elif type == "raid0":
            self.disk = raid.Raid0(name)
        elif type == "raid1":
            self.disk = raid.Raid1(name)

    def nb_blocks(self) -> int:
        return self.disk.nb_blocks()

    def seek(self, addr_block: int) -> int:
        return self.disk.seek(addr_block)

    def read(self, nb_blocks: int) -> bytes:
        return self.disk.read(nb_blocks)

    def write(self, nb_blocks: int, data: bytes) -> int:
        return self.disk.write(nb_blocks, data)
