# import
import os

# code
class disk(object):
    def __init__(self, name: str):
        self.cursor = 0
        self.name = name

    def nb_blocks(self) -> int:
        """return the numbre of blocks of a virtual partition
        """
        file_stats = os.stat(self.name)
        return file_stats.st_size // 512 + int(file_stats.st_size % 512 != 0)*1

    def seek(self, addr_block: int) -> int:
        """move the cursor on the [addr_block] th block of 512 o.
        """
        if self.nb_blocks() <= addr_block:
            return -1
        if addr_block == -1:
            self.cursor = self.nb_blocks() - 1
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


    def write(self, nb_blocks: int, data: str) -> int:
        """write [data] in the block of 512 o on which the cursor is.
        """
        data = data.encode()
        if len(data) != 512 * nb_blocks:
            data += b"\x00" * (nb_blocks * 512 - (len(data) % 512))
        with open(self.name, "rb") as file:
            before = file.read(self.cursor * 512)
            erase = file.read(nb_blocks)
            if self.nb_blocks() - self.cursor * 512 - nb_blocks > 0:
                after = file.read(self.nb_blocks() - self.cursor * 512 - nb_blocks)
            else:
                after = b""
        with open(self.name, "wb") as file:
            file.seek(0)
            file.write(before + data + after)
        return 0
