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
        self.cursor = addr_block
        return 1

    def read(self, nb_blocks: int) -> bytes:
        """read the block of 512 o on which the cursor is.
        """
        if self.cursor + nb_blocks > self.nb_blocks():
            raise IOError("end of file")
        with open(self.name, "r") as file:
            data = file.read()
            return data[self.cursor * 512 :(self.cursor + nb_blocks) * 512].encode()


    def write(self, nb_blocks: int, data: str) -> int:
        """write [data] in the block of 512 o on which the cursor is.
        """
        pass
