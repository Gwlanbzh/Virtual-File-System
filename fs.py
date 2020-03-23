# Formatting a virtual partition.

def init(PATH: str) -> int:
    """Initializes a virtual partition, which needs to be unmounted.
    """
    pass
    
# Unmounting a virtual partition.

def unmount(MNT: str) -> int:
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

# Reading a file's metadatas.

def read_meta(FILE: str) -> meta:
    """Returns a file's metadata as a struct called "meta".
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

def fread(f: file_ptr, nb_blocks: int) -> bytes:
    """Reads nb_blocks blocks of 512 bytes from the file f.
    """
    pass

def fwrite(f: file_ptr, to_write) -> int:
    """Writes some bytes to a file.
    """
    pass
