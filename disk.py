def nb_blocks(name: str) -> int:
    """return the numbre of blocks of a virtual partition
    """
    with open(name, "r") as file:
        data = file.read()
        return len(data)//512 + int(len(data) % 512 != 0)*1

def seek(name: str, addr_block: int) -> int:
    """move the cursor on the [addr_block] th block of 512o.
    """
    pass

def read(name: str, nb_blocks: int) -> str:
    """read the block of 512 o on which the cursor is.
    """
    pass

def write(name: str, nb_blocks: int, data: str) -> int:
    """write [data] in the block of 512 o on which the cursor is.
    """
    pass
