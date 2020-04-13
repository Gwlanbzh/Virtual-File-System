#!usr/bin/python3.6

import fs

WORKING_DIRECTORY = "/"

# ls command


def ls(dir: str = "", mode=""):
    """\x1b[1mNAME:\x1b[0m
    ls - list directory contents

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mls\x1b[0m [FILE] [OPTION]

\x1b[1mDESCRIPTION:\x1b[0m
    List  information  about the FILEs (the current directory by default)

    Mandatory arguments to long options are mandatory for short options too.

    \x1b[1m-l --long\x1b[0m
        print more informations.

    \x1b[1m-d --debug\x1b[0m
        print files locations.
    """
    try:
        if dir == "":
            dir = WORKING_DIRECTORY
        if dir[0] != "/":
            path = WORKING_DIRECTORY + dir
            if path[len(path) - 1] != "/":
                dir = path + "/"
            else:
                dir = path
        else:
            if dir[len(dir) - 1] != "/":
                dir += "/"
        dir_content = fs.ls(dir)
        if dir_content == []:
            print("\x1b[38:5:10m empty dir\x1b[39m")
        for x in dir_content:
            if len(x) == 3:
                if mode == "-d" or mode == "--debug":
                    print(
                        "\x1b[38:5:10m"
                        + x[0].decode()
                        + "/" * int(int(x[2].decode()) == 0)
                        + "  "
                        + " " * (10 - len(x[0].decode()) - 1)
                        + " " * int(int(x[2].decode()) == 1)
                        + str(x[1])
                        + "\x1b[39m"
                    )
                elif mode == "-l" or mode == "--long":
                    print(
                        "\x1b[38:5:10m"
                        + x[0].decode()
                        + "/" * int(int(x[2].decode()) == 0)
                        + "  "
                        + " " * (10 - len(x[0].decode()) - 1)
                        + " " * int(int(x[2].decode()) == 1)
                        + str(len(x[1]) * 512)
                        + "\x1b[39m"
                    )
                else:
                    print(
                        "\x1b[38:5:10m"
                        + x[0].decode()
                        + "/" * int(int(x[2].decode()) == 0)
                        + "   "
                        + "\x1b[39m"
                    )
            else:
                pass
    except SyntaxError as e:
        print(e)


# pwd command:


def pwd():
    """\x1b[1mNAME:\x1b[0m
    pwd - print name of current/working directory

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mpwd\x1b[0m

\x1b[1mDESCRIPTION:\x1b[0m
    Print the full filename of the current working directory.
    """
    print(WORKING_DIRECTORY)


# cd command:


def cd(dir: str = ""):
    """\x1b[1mNAME:\x1b[0m
    cd - change working directory

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mcd\x1b[0m [FILE]

\x1b[1mDESCRIPTION:\x1b[0m
    Change Working directory (the default directory is /)
    """
    try:
        global WORKING_DIRECTORY
        if dir == "" or dir == "/":
            WORKING_DIRECTORY = "/"
        elif dir == ".." or dir == "../":
            if WORKING_DIRECTORY == "/":
                pass
            else:
                data = WORKING_DIRECTORY.split("/")
                PATH = WORKING_DIRECTORY[
                    0 : len(WORKING_DIRECTORY) - len(data[len(data) - 2]) - 1
                ]
                WORKING_DIRECTORY = PATH
        elif dir[0] != "/":
            if dir[len(dir) - 1] != "/":
                data = dir.split("/")
                PATH = dir[0 : len(dir) - len(data[len(data) - 1])]
                if (
                    file_exist(WORKING_DIRECTORY + PATH, data[len(data) - 1])
                    != 0
                ):
                    print("dossier inexistant")
                    return
                WORKING_DIRECTORY += dir + "/"
            else:
                data = dir.split("/")
                PATH = dir[0 : len(dir) - len(data[len(data) - 2]) - 1]
                if (
                    file_exist(WORKING_DIRECTORY + PATH, data[len(data) - 2])
                    != 0
                ):
                    print("dossier inexistant")
                    return
                WORKING_DIRECTORY += dir
        else:
            if dir[len(dir) - 1] != "/":
                data = dir.split("/")
                PATH = dir[0 : len(dir) - len(data[len(data) - 1])]
                if file_exist(PATH, data[len(data) - 1]) != 0:
                    print("dossier inexistant")
                    return
                WORKING_DIRECTORY = dir + "/"
            else:
                data = dir.split("/")
                PATH = dir[0 : len(dir) - len(data[len(data) - 2]) - 1]
                if file_exist(PATH, data[len(data) - 2]) != 0:
                    print("dossier inexistant")
                    return
                WORKING_DIRECTORY = dir
    except SyntaxError as e:
        print("dossier inexistant")


# mkdir


def mkdir(PATH: str, name: str):
    """\x1b[1mNAME:\x1b[0m
    mkdir - make directories

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mmkdir\x1b[0m DIRECTORY

\x1b[1mDESCRIPTION:\x1b[0m
    Create the DIRECTORY(ies), if they do not already exist.
    """
    dir = fs.mkdir(PATH, name)
    if dir == 0:
        print("directory {} sucessfully created".format(PATH + name))
    else:
        print("error")


# rmdir


def rmdir(PATH: str, name: str):
    """\x1b[1mNAME:\x1b[0m
    rmdir - remove empty directories

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mrmdir\x1b[0m DIRECTORY

\x1b[1mDESCRIPTION:\x1b[0m
    Remove the DIRECTORY(ies), if they are empty.
    """
    dir = fs.rmdir(PATH, name)
    if dir == 0:
        print("directory {} sucessfully remove".format(PATH + name))
    else:
        print("invalid directory name or directory not empty")


# touch


def touch(PATH: str, name: str):
    """\x1b[1mNAME:\x1b[0m
    touch - change file timestamps

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mtouch\x1b[0m FILE

\x1b[1mDESCRIPTION:\x1b[0m
    create an empty FILE
    """
    files = [x[0] for x in fs.ls(PATH)]
    if name.encode() in files:
        print("fichier déjà existant")
        return
    try:
        file = fs.fopen(PATH + name, "w")
        file.fwrite(b"\x00".decode())
        file.fclose()
        print("fichier créé")
    except SyntaxError as e:
        print(e)
        return


# cp


def cp(file: str, PATH: str):
    """\x1b[1mNAME:\x1b[0m
    cp - copy files and directories

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mcp\x1b[0m SOURCE DEST

\x1b[1mDESCRIPTION:\x1b[0m
    Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.
    """
    pass


# rm


def rm(PATH: str, file: str, mode=0):
    """\x1b[1mNAME:\x1b[0m
    rm - remove files

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mrm\x1b[0m FILE

\x1b[1mDESCRIPTION:\x1b[0m
    removes specified file.

    Mandatory arguments to long options are mandatory for short options too.

    \x1b[1m-s --secure\x1b[0m
        erase the file content
    """
    if mode == "-s" or mode == "--secure":
        dir = fs.rm(PATH, file, 1)
    else:
        dir = fs.rm(PATH, file, mode)
    if dir == 0:
        print("file {} sucessfully remove".format(PATH + file))
    else:
        print("invalid file")


# mv


def mv(file1: str, file2: str):
    """\x1b[1mNAME:\x1b[0m
    mv - move (rename) files

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mmv\x1b[0m SOURCE DEST

\x1b[1mDESCRIPTION:\x1b[0m
    Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY.
    """
    pass


# cat


def cat(PATH: str, file: str):
    """\x1b[1mNAME:\x1b[0m
    cat - print the file content on the standard output

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mcat\x1b[0m FILE

\x1b[1mDESCRIPTION:\x1b[0m
    print the file content on the standard output.
    """
    files = [x[0] for x in fs.ls(PATH)]
    if file.encode() not in files:
        print("fichier non existant")
        return
    try:
        file = fs.fopen(PATH + file, "r")
        data = file.fread()
        file.fclose()
        for x in data.split("\\n"):
            print(x)
        # print(data)
    except SyntaxError as e:
        print(e)
        return


# tac


def tac(PATH: str, file: str):
    """\x1b[1mNAME:\x1b[0m
    cat - print the file content on the standard output in reverse

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mtac\x1b[0m FILE

\x1b[1mDESCRIPTION:\x1b[0m
    print the file content on the standard output in reverse.
    """
    files = [x[0] for x in fs.ls(PATH)]
    if file.encode() not in files:
        print("fichier non existant")
        return
    try:
        file = fs.fopen(PATH + file, "r")
        data = file.fread()
        file.fclose()
        dat = data.split("\\n")
        for x in range(len(dat)):
            print(dat[len(dat) - x - 1])
    except SyntaxError as e:
        print(e)
        return


# head


def head(PATH: str, file: str):
    """\x1b[1mNAME:\x1b[0m
    head - output the first part of files

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mhead\x1b[0m FILE

\x1b[1mDESCRIPTION:\x1b[0m
    print the first 10 lines of the file on the standard output in reverse.
    """
    files = [x[0] for x in fs.ls(PATH)]
    if file.encode() not in files:
        print("fichier non existant")
        return
    try:
        file = fs.fopen(PATH + "/" + file, "r")
        data = file.fread()
        file.fclose()
        dat = data.split("\\n")
        for x in range(10):
            if x < len(dat):
                print(dat[x])
    except SyntaxError as e:
        print(e)
        return


# tail


def tail(PATH: str, file: str):
    """\x1b[1mNAME:\x1b[0m
    tail - output the last part of files

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mtail\x1b[0m FILE

\x1b[1mDESCRIPTION:\x1b[0m
    print the last 10 lines of the file on the standard output in reverse.
    """
    files = [x[0] for x in fs.ls(PATH)]
    if file.encode() not in files:
        print("fichier non existant")
        return
    try:
        file = fs.fopen(PATH + "/" + file, "r")
        data = file.fread()
        file.fclose()
        dat = data.split("\\n")
        for x in range(10):
            if x < len(dat):
                print(dat[len(data) - x])
    except SyntaxError as e:
        print(e)
        return


# echo


def echo(msg: str, sortie: str = "stdout", mode="w"):
    """\x1b[1mNAME:\x1b[0m
    echo - display a line of text

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mecho\x1b[0m STRING

\x1b[1mDESCRIPTION:\x1b[0m
    Echo the STRING(s) to standard output.
    """
    try:
        if sortie == "stdout":
            print(msg.replace("\\n", "\n"))
        else:
            if sortie[0] == "/":
                file = fs.fopen(sortie, mode)
                file.fwrite(msg.replace("\\n", "\n"))
                file.fclose()
            else:
                file = fs.fopen(WORKING_DIRECTORY + sortie, mode)
                file.fwrite(msg.replace("\\n", "\n"))
                file.fclose()
            print("sucess")
    except SyntaxError as e:
        print("le fichier n'existe pas")


# list


def list():
    """\x1b[1mNAME:\x1b[0m
    list - list all commands

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mlist\x1b[0m

\x1b[1mDESCRIPTION:\x1b[0m
    display the list of all commands
    """
    for x in COMMANDS.keys():
        print("\x1b[38:5:10m " + x + "\x1b[39m")


# man


def man(cmd: str = "man"):
    """\x1b[1mNAME:\x1b[0m
    man - display help

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mman\x1b[0m COMMAND

\x1b[1mDESCRIPTION:\x1b[0m
    display the help of the command
    """
    if cmd not in COMMANDS.keys():
        print("invalid argument")
    else:
        print(COMMANDS[cmd].__doc__)


# exit


def exit():
    """\x1b[1mNAME:\x1b[0m
    exit - exit shell

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mexit\x1b[0m

\x1b[1mDESCRIPTION:\x1b[0m
    exit the shell
    """
    pass


COMMANDS = {
    "ls": ls,
    "cd": cd,
    "pwd": pwd,
    "mkdir": mkdir,
    "rmdir": rmdir,
    "touch": touch,
    "cp": cp,
    "rm": rm,
    "mv": mv,
    "cat": cat,
    "tac": tac,
    "head": head,
    "tail": tail,
    "man": man,
    "echo": echo,
    "list": list,
    "exit": exit,
}


# file exist


def file_exist(PATH: str, file: str) -> bool:
    """retourne 0 si le fichier existe et si c'est un dossier,
       retourne 1 si le fichier existe et si c'est un fichier,
       retourne -1 si le fichier n'existe pas
    """
    dir = fs.ls(PATH)
    for x in dir:
        if x[0] == file.encode():
            return int(x[2].decode())
    return -1


# main


def main():
    while True:
        inp = input(
            "\x1b[38:5:12m" + WORKING_DIRECTORY + "\x1b[38:5:208m $ \x1b[39m"
        )
        cmd = inp.split()
        if len(cmd) == 0 or cmd[0] not in COMMANDS.keys():
            print("invalide command")
        elif cmd[0] == "ls":
            if len(cmd) == 3:
                ls(cmd[1], cmd[2])
            elif len(cmd) == 2:
                if cmd[1] in ("-l", "-d", "--debug"):
                    ls("", cmd[1])
                else:
                    ls(cmd[1])
            else:
                ls("")
        elif cmd[0] == "cd":
            if len(cmd) > 1:
                cd(cmd[1].replace(" ", ""))
            else:
                cd("")
        elif cmd[0] == "pwd":
            pwd()
        elif cmd[0] == "mkdir":
            if len(cmd) == 2:
                mkdir(WORKING_DIRECTORY, cmd[1])
            elif len(cmd) == 3:
                mkdir(cmd[1], cmd[2])
            else:
                print("argument error")
        elif cmd[0] == "rmdir":
            if len(cmd) == 2:
                rmdir(WORKING_DIRECTORY, cmd[1])
            elif len(cmd) == 3:
                rmdir(cmd[1], cmd[2])
            else:
                print("argument error")
        elif cmd[0] == "rm":
            if len(cmd) == 2:
                rm(WORKING_DIRECTORY, cmd[1])
            elif len(cmd) == 3:
                if cmd[2] == "-s" or cmd[2] == "--secure":
                    rm(WORKING_DIRECTORY, cmd[1], cmd[2])
                else:
                    rm(cmd[1], cmd[2])
            elif len(cmd) == 4:
                rm(cmd[1], cmd[2], cmd[3])
            else:
                print("argument error")
        elif cmd[0] == "man":
            if len(cmd) > 1:
                man(cmd[1])
            else:
                man()
        elif cmd[0] == "touch":
            if len(cmd) == 2:
                touch(WORKING_DIRECTORY, cmd[1])
            elif len(cmd) == 3:
                touch(cmd[1], cmd[2])
        elif cmd[0] == "cat":
            if len(cmd) == 2:
                cat(WORKING_DIRECTORY, cmd[1])
            elif len(cmd) == 3:
                cat(cmd[1], cmd[2])
            else:
                print("argument error")
        elif cmd[0] == "tac":
            if len(cmd) == 2:
                tac(WORKING_DIRECTORY, cmd[1])
            elif len(cmd) == 3:
                tac(cmd[1], cmd[2])
            else:
                print("argument error")
        elif cmd[0] == "echo":
            data = inp.split(">>")
            if len(data) == 1:
                data = inp.split(">")
                if len(data) == 1:
                    echo(data[0][5 : len(data[0])])
                elif len(data) == 2:
                    echo(
                        data[0][5 : len(data[0]) - 1],
                        data[1][1 : len(data[1])],
                        "w",
                    )
                else:
                    print("argument error")
            elif len(data) == 2:
                echo(
                    data[0][5 : len(data[0]) - 1],
                    data[1][1 : len(data[1])],
                    "a",
                )
            else:
                print("argument error")
        elif cmd[0] == "head":
            if len(cmd) == 2:
                head(WORKING_DIRECTORY, cmd[1])
            elif len(cmd) == 3:
                head(cmd[1], cmd[2])
            else:
                print("argument error")
        elif cmd[0] == "tail":
            if len(cmd) == 2:
                tail(WORKING_DIRECTORY, cmd[1])
            elif len(cmd) == 3:
                tail(cmd[1], cmd[2])
            else:
                print("argument error")
        elif cmd[0] == "list":
            list()
        elif cmd[0] == "exit":
            exit()
            break


#

if __name__ == "__main__":
    main()
