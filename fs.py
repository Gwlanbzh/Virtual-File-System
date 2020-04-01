import disk
DISK = "" # disk location
ROOT_LOCATION = 1 # root dir location

# Formatting a virtual partition.

def init(PATH: str) -> int:
    """Initializes a virtual partition, which needs to be unmounted.
    """
    pass

# Mounting a virtual partition.

def mount_dsk(PATH: str) -> int:
    """Mounts the virtual partition.
    """
    pass

def umount_dsk(MNT: str) -> int:
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
    diskfile.seek(ROOT_LOCATION)
    emplacement = 1
    i = 1
    while True:
        diskfile.seek(emplacement)
        dir = diskfile.read(1)
        data = dir.replace(b"\x00", b"").split(";".encode())
        data[0] = data[0][1:len(data[0])]
        data[len(data) - 1] = data[len(data) - 1][0:len(data[len(data) - 1]) - 1]
        for x in data:
            if path[i] == "":
                return [x[0:-6] for x in data]
            if path[i].encode() in x:
                i += 1
                emplacement = int(x[-4:-1])
                break


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
