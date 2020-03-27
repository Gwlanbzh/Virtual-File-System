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

def ls(DIR: str) -> str:
    """Read a directory's content.
    """
    pass

# Entry appending and deletion in a directory.

def mkdir(parent_dir, NAME: str) -> int:
    """Creates an empty directory.
    """
    pass

def rmkdir(parent_dir, NAME: str) -> int:
    """Delete an empty directory.
    """
    pass

# Opening and closing of a file.

def fopen(FILE: str, mode: char) -> file_ptr:
    """Opens a file.
    """
    pass

def fclose(f: file_ptr) -> int:
    """Closes a file.
    """
    pass

# positionning the cursor to the beginning of a file.

def seek_file_beg(FILE: str) -> int:
    """Positions the cursor at the beginning of a file.
    """
    pass

# Reading and writing to a file.

def fread(f: file_ptr) -> bytes:
    """Reads the file f.
    """
    pass

def fwrite(f: file_ptr, to_write) -> int:
    """Writes some bytes to a file.
    """
    pass
