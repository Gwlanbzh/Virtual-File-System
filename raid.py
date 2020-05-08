from disk import Disk


class Raid0(object):
    def __init__(self, name: str):
        self.disk1 = Disk(name + "1")
        self.disk2 = Disk(name + "2")

    def nb_blocks(self) -> int:
        nb1 = self.disk1.nb_blocks()
        return nb1

    def seek(self, addr_block: int) -> int:
        a = self.disk1.seek(addr_block)
        b = self.disk2.seek(addr_block)
        return a

    def read(self, nb_blocks: int) -> bytes:
        a = self.disk1.read(nb_blocks)
        b = self.disk2.read(nb_blocks)
        return a

    def write(self, nb_blocks: int, data: bytes) -> int:
        a = self.disk1.write(nb_blocks, data)
        b = self.disk2.write(nb_blocks, data)
        return a


class Raid1(object):
    def __init__(self, name: str):
        self.disk1 = Disk(name + "1")
        self.disk2 = Disk(name + "2")
        self.cursor = 0

    def nb_blocks(self) -> int:
        """
        """
        return self.disk1.nb_blocks() + self.disk2.nb_blocks()

    def seek(self, addr_block: int) -> int:
        if self.nb_blocks() < addr_block:
            return -1
        if addr_block == -1:
            self.cursor = self.nb_blocks()
            return 0
        self.cursor = addr_block
        return 0

    def read(self, nb_blocks: int) -> bytes:
        """
        """
        if nb_blocks == 1:
            if self.cursor % 2 == 0:
                self.disk1.seek(self.cursor // 2)
                return self.disk1.read(1)
            else:
                self.disk2.seek(self.cursor // 2)
                return self.disk2.read(1)
        else:
            data = b""
            for x in range(nb_blocks):
                if x % 2 == 0:
                    self.disk1.seek((self.cursor + x) // 2)
                    data += self.disk1.read(1)
                else:
                    self.disk2.seek((self.cursor + x) // 2)
                    data += self.disk2.read(1)
            return data

    def write(self, nb_blocks: int, data: bytes) -> int:
        """
        """
        if len(data) > nb_blocks * 512:
            return -1
        if len(data) != 512 * nb_blocks:
            data += b"\x00" * (nb_blocks * 512 - len(data))
        if nb_blocks == 1:
            if self.cursor % 2 == 0:
                self.disk1.seek(self.cursor // 2)
                self.cursor += 1
                return self.disk1.write(1, data)
            else:
                self.disk2.seek(self.cursor // 2)
                self.cursor += 1
                return self.disk2.write(1, data)
        else:
            a = 0
            for x in range(len(data) // 512 + 1 * int(len(data) % 512)):
                if a == -1:
                    return -1
                if (self.cursor + x) % 2 == 0:
                    self.disk1.seek((self.cursor + x) // 2)
                    a = self.disk1.write(1, data[x * 512 : (x + 1) * 512])
                else:
                    self.disk2.seek((self.cursor + x) // 2)
                    a = self.disk2.write(1, data[x * 512 : (x + 1) * 512])
        self.cursor += nb_blocks
