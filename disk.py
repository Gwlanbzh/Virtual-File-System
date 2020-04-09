# import
import os

# code
class Disk(object):
    def __init__(self, name: str):
        self.cursor = 0
        self.name = name

    def nb_blocks(self) -> int:
        """return the numbre of blocks of a virtual partition
        """
        file_stats = os.stat(self.name)
        return (
            file_stats.st_size // 512 + int(file_stats.st_size % 512 != 0) * 1
        )

    def seek(self, addr_block: int) -> int:
        """move the cursor on the [addr_block] th block of 512 o.
        """
        if self.nb_blocks() < addr_block:
            return -1
        if addr_block == -1:
            self.cursor = self.nb_blocks()
            return 0
        self.cursor = addr_block
        return 0

    def read(self, nb_blocks: int) -> bytes:
        """read the block of 512 o on which the cursor is.
        """
        if self.cursor + nb_blocks > self.nb_blocks():
            raise IOError("end of file")
        with open(self.name, "rb") as file:
            file.seek(self.cursor * 512)
            return file.read(nb_blocks * 512)

    def write(self, nb_blocks: int, data: bytes) -> int:
        """write [data] in the block of 512 o on which the cursor is.
        """
        if len(data) > nb_blocks * 512:
            return -1
        if len(data) != 512 * nb_blocks:
            data += b"\x00" * (nb_blocks * 512 - len(data))
        try:
            f = open(self.name, "r+b")
        except IOError:
            f = open(self.name, "wb")
        f.seek(self.cursor * 512)
        f.write(data)
        self.cursor += nb_blocks
        f.close()
        return 0
