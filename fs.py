import disk
DISK = "" # disk location
ROOT_LOCATION = 1 # root dir location

# Formatting a virtual partition.

def init(PATH: str, size: int) -> int:
    """Initializes a virtual partition, which needs to be unmounted.
    """
    pass

# Mounting a virtual partition.

def unmount(MNT: str) -> int:
    """Umounts the virtual partition.
    """
    pass

# Reading a directory's content.

def ls(DIR: str) -> list:
    """Read a directory's content.
    """
    path = DIR.split("/")
    if path[0] == "" and path[len(path) - 1] == "":
        path[0] = "/"
    else:
        raise SyntaxError("invalid path")
    diskfile = disk.disk(DISK)
    emplacement = [ROOT_LOCATION]
    i = 1
    while True:
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
                emplacement = [int(y) for y in x[1]]
                #print(emplacement)
                break
            else:
                raise SyntaxError("invalid path")


# Entry appending and deletion in a directory.

def mkdir(parent_dir, NAME: str) -> int:
    """Creates an empty directory.
    """
    pass

def rmdir(parent_dir, NAME: str) -> int:
    """Delete an empty directory.
    """
    pass

# Opening and closing of a file.

def fopen(FILE: str, mode: str):
    """Opens a file.
    """
    pass

def fclose(f) -> int:
    """Closes a file.
    """
    pass

# positionning the cursor to the beginning of a file.

def seek_file_beg(FILE: str) -> int:
    """Positions the cursor at the beginning of a file.
    """
    pass

# Reading and writing to a file.

def fread(f) -> bytes:
    """Reads the file f.
    """
    pass

def fwrite(f, to_write) -> int:
    """Writes some bytes to a file.
    """
    pass
