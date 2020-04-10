from disk import Disk


class Cache(object):
    def __init__(self, name: str):
        self.disk = Disk(name)

    def nb_blocks(self) -> int:
        return self.disk.nb_blocks()

    def seek(self, addr_block: int) -> int:
        return self.disk.seek(addr_block)

    def read(self, nb_blocks: int) -> bytes:
        return self.disk.read(nb_blocks)

    def write(self, nb_blocks: int, data: bytes) -> int:
        return self.disk.write(nb_blocks, data)
