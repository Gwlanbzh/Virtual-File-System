def init(name: str):
    """Initializes a virtual partition.
    """
    pass

def nb_blocks(name: str) - int:
    """return the numbre of blocks of a virtual partition
    """
    pass

def seek(name: str, addr_block: int):
    """move the cursor on the [addr_block] th block of 512o.
    """
    pass

def read(name: str, nb_blocks: int):
    """read the block of 512 o on which the cursor is.
    """
    pass

def write(name: str, nb_blocks: int, data: str):
    """write [data] in the block of 512 o on which the cursor is.
    """
    pass
