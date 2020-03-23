class disk:
    def __init__(self, name: str):
        self.cursor = 0
        self.name = name
        
    def nb_blocks(self) -> int:
        """return the numbre of blocks of a virtual partition
        """
        with open(self.name, "r") as file:
            data = file.read()
            return len(data) // 512 + int(len(data) % 512 != 0)*1

    def seek(self, addr_block: int) -> int:
        """move the cursor on the [addr_block] th block of 512 o.
        """
        if self.nb_blocks() > addr_block:
            self.cursor = addr_block
            return 1
        else:
            return -1

    def read(self, nb_blocks: int) -> bytes:
        """read the block of 512 o on which the cursor is.
        """
        if self.cursor + nb_blocks <= self.nb_blocks():
            with open(self.name, "r") as file:
                data = file.read()
                return data[self.cursor * 512 :(self.cursor + nb_blocks) * 512].encode()
        else:
            raise IOError("end of file")

    def write(self, nb_blocks: int, data: str) -> int:
        """write [data] in the block of 512 o on which the cursor is.
        """
        pass
