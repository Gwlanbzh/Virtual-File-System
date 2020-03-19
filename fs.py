# Formatting a virtual partition.

def init(PATH: str) -> int:
    """Initializes a virtual partition, which needs to be unmounted.
    """
    
# Mounting a virtual partition.

def mount_dsk(PATH: str) -> int:
    """mounts the virtual partition.
    """

def umount_dsk(MNT: str) -> int:
    """umounts the virtual partition.
    """

# Reading a directory's content.

ls(DIR: str) -> str:
    """Read a directory's content.
    """

# Entry appending and deletion in a directory.

mkdir(parent_dir, NAME: str) -> int:
    """Creates an empty directory.
    """

# Reading a file's metadatas.

read_meta(FILE: str) -> meta:
    """Returns a file's metadata as a struct called "meta".
    """

# Opening and closing of a file.

def fopen(FILE: str, mode: char) -> file_ptr:
    """Opens a file.
    """

def fclose(f: file_ptr) -> int:
    """Closes a file.
    """

# positionning the cursor to the beginning of a file.

def seek_file_beg(FILE: str) -> int:
    """position the cursor at the beginning of a file.
    """

# Reading and writing to a file.

def fread(f: file_ptr, nb_blocks: int) -> bytes:
    """Reads nb_blocks blocks of 512 bytes from the file f.
    """

def fwrite(f: file_ptr, to_write) -> int:
    """write some bytes to a file.
    """
