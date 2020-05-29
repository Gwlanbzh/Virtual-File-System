import fs
from sys import argv


def bytes_to_ascii(byte):
    if (
        int.from_bytes(byte, "big") >= 33
        and int.from_bytes(byte, "big") <= 126
    ):
        return byte.decode()
    else:
        return "."


def main(path):
    fd = fs.fopen(path, "rb")
    data = fd.fread()
    fd.fclose()
    i = 0
    lines = []
    r = "{0:08x}: ".format(i + 1)
    ascii_form = ""
    while i < len(data):
        r += "{0:02x}".format(data[i])
        ascii_form += bytes_to_ascii(bytes([data[i]]))
        if i % 2 == 1:
            r += " "
        if i % 16 == 15:
            r += ascii_form
            ascii_form = ""
            r += "\n{0:08x}: ".format(i + 1)
        i += 1
    r += " " * (66 - len(r.split("\n")[-1]) - 16) + ascii_form
    return r


if __name__ == "__main__":
    fs.open(argv[1])
    print(main(argv[2]))
