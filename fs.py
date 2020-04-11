from cache import Cache
import math

DISK = "~/projects/fs/disk.dsk"  # disk location
ROOT_LOCATION = 0  # root dir location

# file globals var

FILE_NAME_SIZE = 10
CHARS_ALLOWED = (
    "AZERTYUIOPQSDFGHJKLMWXCVBNazertyuiopqsdfghjklmwxcvbn1234567890"
)


# Formatting a virtual partition.


def init(PATH: str, size: int) -> int:
    """Initializes a virtual partition, which needs to be unmounted.
    """
    global DISK
    global ROOT_LOCATION
    if size > 65535:
        raise ValueError("unallowed size (too large)")
    DISK = PATH
    table_size = int(
        math.ceil(size / (512 * 8))
    )  # 512 * 8 stands for the number of bytes in a block, multiplied by the number of bits in a byte, since we use 1 bit by block.
    bin_table_size = bytes([table_size // 256, table_size % 256])
    ROOT_LOCATION = table_size
    new_disk = Cache(PATH)
    new_disk.write(size, bin_table_size + b"\x80")


# Mounting a virtual partition.


def unmount(MNT: str) -> int:
    """Umounts the virtual partition.
    """
    pass


# Reading a directory's content.


def ls(DIR: str) -> list:
    """Read a directory's content.
    """
    # print("-" + DIR + "-")
    path = DIR.split("/")
    if path[0] == "" and path[len(path) - 1] == "":
        path[0] = "/"
    else:
        raise SyntaxError("invalid path : " + DIR)
    diskfile = Cache(DISK)
    emplacement = [ROOT_LOCATION]
    i = 1
    while True:
        exist = False
        dir = b""
        for x in emplacement:
            diskfile.seek(x)
            dir += diskfile.read(1)
        data = dir.replace(b"\x00", b"").split(";".encode())
        data = [x.split(":".encode()) for x in data]
        for x in range(len(data)):
            for y in range(len(data[x])):
                if y == 1:
                    data[x][y] = data[x][y].split("+".encode())
        for x in data:
            if path[i] == "":
                return data
            if path[i].encode() in x and x[2] == b"0":
                i += 1
                exist = True
                emplacement = [int(y) for y in x[1]]
                break
        if exist == False:
            raise SyntaxError("invalid path : " + DIR)


# Entry appending and deletion in a directory.


def mkdir(parent_dir, NAME: str) -> int:
    """Creates an empty directory.
    """
    if len(NAME) > FILE_NAME_SIZE:
        raise SyntaxError("bad file name")
    for i in NAME:
        if i not in CHARS_ALLOWED:
            raise SyntaxError("bad file name")
    try:
        dir_content = ls(parent_dir)
        if NAME.encode() in [x[0] for x in dir_content]:
            return -1
        nex_loc = free_block()
        use_block(nex_loc)
        disk = Cache(DISK)
        disk.seek(nex_loc)
        disk.write(1, "".encode())
        set_location(parent_dir, NAME, [str(nex_loc).encode()], b"0")
        return 0
    except SyntaxError as e:
        return -1


def rmdir(parent_dir, NAME: str) -> int:
    """Delete an empty directory.
    """
    if NAME.encode() not in [x[0] for x in ls(parent_dir)]:
        return -1
    if ls(parent_dir + NAME + "/") != [[b""]]:
        return -1
    parent_dir_content = ls(parent_dir)
    for x in parent_dir_content:
        if x[0] == NAME.encode():
            loc = x[1]
    new_parent_dir_content = [y for y in parent_dir_content if y[1] != loc]
    disk = Cache(DISK)
    loc_up_dir = [str(ROOT_LOCATION).encode()]
    if parent_dir != "/":
        up_dir = parent_dir.split("/")
        up_dir_parent = parent_dir[
            0 : len(parent_dir) - len(up_dir[len(up_dir) - 2]) - 1
        ]
        for i in ls(up_dir_parent):
            if i[0] == up_dir[len(up_dir) - 2].encode():
                loc_up_dir = i[1]
    data = ""
    for x in new_parent_dir_content:
        if len(x) > 1:
            loc_ = ""
            for y in x[1]:
                loc_ += "{:0>3d}".format(int(y.decode()))
                loc_ += "+"
            loc_ = loc_[0 : len(loc_) - 1]
            data += x[0].decode()
            data += ":"
            data += loc_
            data += ":"
            data += x[2].decode()
            data += ";"
    data = data[0 : len(data) - 1]

    for x in range(len(loc_up_dir)):
        disk.seek(int(loc_up_dir[x].decode()))
        disk.write(1, data[x * 512 : (x + 1) * 512].encode())
    for x in loc:
        use_block(int(x.decode()), "0")

    # print(parent_dir_content, new_parent_dir_content)
    return 0


# rm


def rm(parent_dir, NAME: str, mode=0):
    """delete a file (mode 1 = secure)
    """
    try:
        ls(parent_dir)
    except SyntaxError as e:
        return -1
    if NAME.encode() not in [x[0] for x in ls(parent_dir)]:
        return -1

    parent_dir_content = ls(parent_dir)
    for x in parent_dir_content:
        if x[0] == NAME.encode():
            loc = x[1]
    new_parent_dir_content = [y for y in parent_dir_content if y[1] != loc]
    disk = Cache(DISK)
    loc_up_dir = [str(ROOT_LOCATION).encode()]
    if parent_dir != "/":
        up_dir = parent_dir.split("/")
        up_dir_parent = parent_dir[
            0 : len(parent_dir) - len(up_dir[len(up_dir) - 2]) - 1
        ]
        for i in ls(up_dir_parent):
            if i[0] == up_dir[len(up_dir) - 2].encode():
                loc_up_dir = i[1]
    data = ""
    # print(loc_up_dir)
    for x in new_parent_dir_content:
        if len(x) > 1:
            loc_ = ""
            for y in x[1]:
                loc_ += "{:0>3d}".format(int(y.decode()))
                loc_ += "+"
            loc_ = loc_[0 : len(loc_) - 1]
            data += x[0].decode()
            data += ":"
            data += loc_
            data += ":"
            data += x[2].decode()
            data += ";"
    data = data[0 : len(data) - 1]
    for x in range(len(loc_up_dir)):
        disk.seek(int(loc_up_dir[x].decode()))
        disk.write(1, data[x * 512 : (x + 1) * 512].encode())

    if mode == 1:
        for x in range(len(loc)):
            disk.seek(int(loc[x].decode()))
            disk.write(1, b"\x00")
    for x in loc:
        use_block(int(x.decode()), "0")

    # print(parent_dir_content, new_parent_dir_content)
    return 0


# set location


def set_location(PATH: str, file: str, loc: list, state=b"1"):
    dir_content = ls(PATH)
    loc_file = None
    for x in range(len(dir_content)):
        if dir_content[x][0] == file.encode():
            loc_file = dir_content[x][1]
            break
    if loc_file == None:
        dir_content.append([file.encode(), [x for x in loc], state])
    else:
        if loc_file == loc:
            return 0
        dir_content[x][1] = loc
    if PATH != "/":
        dir = PATH.split("/")
        dir_name = dir[len(dir) - 2]
        up_dir = PATH[0 : len(PATH) - len(dir_name) - 1]
        up_dir_content = ls(up_dir)
        for x in up_dir_content:
            if x[0] == dir_name.encode():
                loc_dir = x[1]
    else:
        loc_dir = [str(ROOT_LOCATION).encode()]
    disk = Cache(DISK)
    data = ""
    # print(dir_content)
    for x in dir_content:
        if len(x) > 1:
            loc_ = ""
            for y in x[1]:
                loc_ += "{:0>3d}".format(int(y.decode()))
                loc_ += "+"
            loc_ = loc_[0 : len(loc_) - 1]
            data += x[0].decode()
            data += ":"
            data += loc_
            data += ":"
            data += x[2].decode()
            data += ";"
    data = data[0 : len(data) - 1]
    for x in range(len(data) // 512 + 1 * int(len(data) % 512 != 0)):
        disk.seek(int(loc_dir[x].decode()))
        disk.write(1, data[x * 512 : (x + 1) * 512 - 1].encode())
    return 0

    # print(loc)


# free block


def free_block():
    """return the first block which is unused
    """
    disk = Cache(DISK)
    disk.seek(0)
    data = disk.read(1)
    nb_block_table = int.from_bytes(data[0:2], byteorder="big")
    disk.seek(0)
    data = disk.read(len(bin(nb_block_table)))
    data = data[2 : len(data)]
    data_bin = bin(int.from_bytes(data, byteorder="big"))
    data_bin = str(data_bin)[2 : len(data_bin)]
    for x in range(len(data_bin)):
        if data_bin[x] != "1":
            return x + ROOT_LOCATION


# set a bloc to used statut


def use_block(block: int, state="1"):
    disk = Cache(DISK)
    disk.seek(0)
    data = disk.read(1)
    nb_block_table_bytes = data[0:2]
    nb_block_table = int.from_bytes(data[0:2], byteorder="big")
    disk.seek(0)
    data = disk.read(len(bin(nb_block_table)))
    data = data[2 : len(data)]
    data_bin = bin(int.from_bytes(data, byteorder="big"))
    data_bin = str(data_bin)[2 : len(data_bin)]
    data_bin_new = ""
    for x in range(len(data_bin)):
        if x != (block - ROOT_LOCATION):
            data_bin_new += data_bin[x]
        else:
            data_bin_new += state
    data_bytes_new = bytes([ROOT_LOCATION // 256, ROOT_LOCATION % 256])
    for x in range(len(data_bin_new) // 8):
        data_bytes_new += bytes([int(data_bin_new[x * 8 : (x + 1) * 8], 2)])
    disk.write(ROOT_LOCATION, data_bytes_new)


# Opening and closing of a file.


class fopen(object):
    def __init__(self, PATH: str, mode: str):
        """Opens a file.
        """
        try:
            self.path = PATH
            self.mode = mode
            dir = PATH.split("/")
            self.dir = PATH[0 : len(PATH) - len(dir[len(dir) - 1])]
            self.name = dir[len(dir) - 1]
            if len(self.name) > FILE_NAME_SIZE:
                raise SyntaxError("bad file name")
            for i in self.name:
                if i not in CHARS_ALLOWED:
                    raise SyntaxError("bad file name")
            dir_content = ls(self.dir)
            self.location = [[b""]]
            for x in dir_content:
                if x[0] == self.name.encode():
                    self.location = x[1]
            if self.location == [[b""]]:
                bloc = free_block()
                self.location = [str(bloc).encode()]
                use_block(free_block())
        except SyntaxError as e:
            raise e

    def fclose(self) -> int:
        """Closes a file.
        """
        pass

    # positionning the cursor to the beginning of a file.

    def seek_file_beg(self) -> int:
        """Positions the cursor at the beginning of a file.
        """
        pass

    # Reading and writing to a file.

    def fread(self) -> bytes:
        """Reads the file f.
        """
        if self.mode == "w":
            raise Exception("file not readable")
        disk = Cache(DISK)
        data = b""
        for x in self.location:
            disk.seek(int(x.decode()))
            data += disk.read(1)
        return data.replace(b"\x00", b"").decode()

    def fwrite(self, to_write: str) -> int:
        """Writes some bytes to a file.
        """
        disk = Cache(DISK)
        for x in self.location:
            disk.seek(int(x.decode()))
            disk.write(1, b"")

        if self.mode == "r":
            raise Exception("file not writable")
        elif self.mode == "w":
            disk = Cache(DISK)
            data = to_write.encode()
            for x in range(len(data) // 512 + 1 * int(len(data) % 512 != 0)):
                if x < len(self.location):
                    disk.seek(int(self.location[x].decode()))
                    disk.write(1, data[x * 512 : (x + 1) * 512 - 1])
                else:
                    bloc = free_block()
                    use_block(bloc)
                    self.location.append(str(bloc).encode())
                    disk.seek(bloc)
                    disk.write(1, data[x * 512 : (x + 1) * 512 - 1])
            while x < (len(self.location) - 1):
                print(x)
                use_block(int(self.location[x + 1].decode()), "0")
                self.location.pop(x + 1)
                x += 1
            dir_content = ls(self.dir)
            for y in self.location:
                use_block(int(y.decode()))
            set_location(self.dir, self.name, self.location)

        return 0
