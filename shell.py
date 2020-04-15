#!usr/bin/env python3

import argparse
import fs

WORKING_DIRECTORY = "/"

# unknown command


def unknown_cmd(arguments: list):
    """unknown command
    """
    print("invalid command")


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


# size


def size(PATH: str, file: str) -> int:
    dir_size = 0
    if file_exist(PATH, file) == 0:
        dir = fs.ls(PATH + file + "/")
        for x in dir:
            if x[2] == b"1":
                dir_size += len(x[1])
            else:
                dir_size += size(PATH + file + "/", x[0].decode())
    elif file_exist(PATH, file) == 1:
        dir = fs.ls(PATH)
        for x in dir:
            if x[0].decode() == file:
                return len(x[1])
    return dir_size


# ls command


def ls(arguments: list):
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", default="False")
    parser.add_argument("-l", "--long", action="store_true", default="False")
    parser.add_argument("-a", "--all", action="store_true", default="False")
    parser.add_argument(
        "directory", type=str, action="store", default="", nargs="?"
    )
    args = parser.parse_args(arguments.split())
    dir = args.directory
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
        new_list = []
        for x in dir_content:
            new_list.append([int(x[2].decode()), x[0], x[1]])
        new_new_list = sorted(new_list)
        for x in new_new_list:
            if len(x) == 3:
                dir_size = size(dir, x[1].decode()) * 512
                if x[1].decode()[0] != "." or args.all == True:
                    print(
                        "\x1b[38:5:10m"
                        + x[1].decode()
                        + "/" * int(x[0] == 0)
                        + "  "
                        + " " * (10 - len(x[1].decode()) - 1)
                        + " " * int(x[0] == 1)
                        + str(x[2]) * int(args.debug == True)
                        + " "
                        * (10 - len(x[1].decode()) - 1)
                        * int(args.debug == True)
                        + (str(dir_size) + "o") * int(args.long == True)
                        + "\x1b[39m"
                    )
    except SyntaxError as e:
        print(e)


# pwd command:


def pwd(argument: list):
    """\x1b[1mNAME:\x1b[0m
    pwd - print name of current/working directory

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mpwd\x1b[0m

\x1b[1mDESCRIPTION:\x1b[0m
    Print the full filename of the current working directory.
    """
    print(WORKING_DIRECTORY)


# cd command:


def cd(arguments: list):
    """\x1b[1mNAME:\x1b[0m
    cd - change working directory

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mcd\x1b[0m [FILE]

\x1b[1mDESCRIPTION:\x1b[0m
    Change Working directory (the default directory is /)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory", type=str, action="store", default="", nargs="?"
    )
    args = parser.parse_args(arguments.split())
    dir = args.directory

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


def mkdir(arguments: list):  # PATH: str, name: str):
    """\x1b[1mNAME:\x1b[0m
    mkdir - make directories

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mmkdir\x1b[0m DIRECTORY

\x1b[1mDESCRIPTION:\x1b[0m
    Create the DIRECTORY(ies), if they do not already exist.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", type=str, action="store", default="", nargs="?"
    )
    parser.add_argument(
        "name", type=str, action="store", default="", nargs="?"
    )
    args = parser.parse_args(arguments.split())
    if args.path == "" and args.name == "":
        print("error")
        return
    if args.path != "" and args.name == "":
        PATH = WORKING_DIRECTORY
        name = args.path
    else:
        PATH = args.path
        name = args.name

    try:
        dir = fs.mkdir(PATH, name)
        if dir == 0:
            print("directory {} sucessfully created".format(PATH + name))
        else:
            print("error")
    except SyntaxError as e:
        print(e)


# rmdir


def rmdir(arguments: list):
    """\x1b[1mNAME:\x1b[0m
    rmdir - remove empty directories

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mrmdir\x1b[0m DIRECTORY

\x1b[1mDESCRIPTION:\x1b[0m
    Remove the DIRECTORY(ies), if they are empty.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", type=str, action="store", default="", nargs="?"
    )
    parser.add_argument(
        "name", type=str, action="store", default="", nargs="?"
    )
    args = parser.parse_args(arguments.split())
    if args.path == "" and args.name == "":
        print("error")
        return
    if args.path != "" and args.name == "":
        PATH = WORKING_DIRECTORY
        name = args.path
    else:
        PATH = args.path
        name = args.name
    dir = fs.rmdir(PATH, name)
    if dir == 0:
        print("directory {} sucessfully remove".format(PATH + name))
    else:
        print("invalid directory name or directory not empty")


# touch


def touch(arguments: list):
    """\x1b[1mNAME:\x1b[0m
    touch - change file timestamps

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mtouch\x1b[0m FILE

\x1b[1mDESCRIPTION:\x1b[0m
    create an empty FILE
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", type=str, action="store", default="", nargs="?"
    )
    parser.add_argument(
        "name", type=str, action="store", default="", nargs="?"
    )
    args = parser.parse_args(arguments.split())
    if args.path == "" and args.name == "":
        print("error")
        return
    if args.path != "" and args.name == "":
        PATH = WORKING_DIRECTORY
        name = args.path
    else:
        PATH = args.path
        name = args.name
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


def cp(arguments: list):
    """\x1b[1mNAME:\x1b[0m
    cp - copy files and directories

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mcp\x1b[0m SOURCE DEST

\x1b[1mDESCRIPTION:\x1b[0m
    Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.
    """
    pass


# rm


def rm(arguments: list):  # PATH: str, file: str, mode=0):
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--secure", action="store_true", default="False")
    parser.add_argument(
        "path", type=str, action="store", default="", nargs="?"
    )
    parser.add_argument(
        "file", type=str, action="store", default="", nargs="?"
    )
    args = parser.parse_args(arguments.split())
    if args.path == "" and args.file == "":
        print("error")
        return
    if args.path != "" and args.file == "":
        PATH = WORKING_DIRECTORY
        file = args.path
    else:
        PATH = args.path
        file = args.file

    dir = fs.rm(PATH, file, int(bool(args.secure)))
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


def cat(arguments: list):
    """\x1b[1mNAME:\x1b[0m
    cat - print the file content on the standard output

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mcat\x1b[0m FILE

\x1b[1mDESCRIPTION:\x1b[0m
    print the file content on the standard output.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", type=str, action="store", default="", nargs="?"
    )
    parser.add_argument(
        "file", type=str, action="store", default="", nargs="?"
    )
    args = parser.parse_args(arguments.split())
    if args.path == "" and args.file == "":
        print("error")
        return
    if args.path != "" and args.file == "":
        PATH = WORKING_DIRECTORY
        file = args.path
    else:
        PATH = args.path
        file = args.file
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


def tac(arguments: list):
    """\x1b[1mNAME:\x1b[0m
    cat - print the file content on the standard output in reverse

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mtac\x1b[0m FILE

\x1b[1mDESCRIPTION:\x1b[0m
    print the file content on the standard output in reverse.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", type=str, action="store", default="", nargs="?"
    )
    parser.add_argument(
        "file", type=str, action="store", default="", nargs="?"
    )
    args = parser.parse_args(arguments.split())
    if args.path == "" and args.file == "":
        print("error")
        return
    if args.path != "" and args.file == "":
        PATH = WORKING_DIRECTORY
        file = args.path
    else:
        PATH = args.path
        file = args.file

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


def head(arguments: list):
    """\x1b[1mNAME:\x1b[0m
    head - output the first part of files

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mhead\x1b[0m FILE

\x1b[1mDESCRIPTION:\x1b[0m
    print the first 10 lines of the file on the standard output in reverse.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", type=str, action="store", default="", nargs="?"
    )
    parser.add_argument(
        "file", type=str, action="store", default="", nargs="?"
    )
    args = parser.parse_args(arguments.split())
    if args.path == "" and args.file == "":
        print("error")
        return
    if args.path != "" and args.file == "":
        PATH = WORKING_DIRECTORY
        file = args.path
    else:
        PATH = args.path
        file = args.file

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


def tail(arguments: list):
    """\x1b[1mNAME:\x1b[0m
    tail - output the last part of files

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mtail\x1b[0m FILE

\x1b[1mDESCRIPTION:\x1b[0m
    print the last 10 lines of the file on the standard output in reverse.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", type=str, action="store", default="", nargs="?"
    )
    parser.add_argument(
        "file", type=str, action="store", default="", nargs="?"
    )
    args = parser.parse_args(arguments.split())
    if args.path == "" and args.file == "":
        print("error")
        return
    if args.path != "" and args.file == "":
        PATH = WORKING_DIRECTORY
        file = args.path
    else:
        PATH = args.path
        file = args.file

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
                print(dat[len(dat) - x - 1])
    except SyntaxError as e:
        print(e)
        return


# echo


def echo(arguments: str):  # msg: str, sortie: str = "stdout", mode="w"):
    """\x1b[1mNAME:\x1b[0m
    echo - display a line of text

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mecho\x1b[0m STRING

\x1b[1mDESCRIPTION:\x1b[0m
    Echo the STRING(s) to standard output.
    """
    args = arguments.split()
    sortie = "stdout"
    msg = ""
    for x in args:
        msg += x
        msg += " "
    if args[len(args) - 2] in (">", ">>"):
        if args[len(args) - 2] == ">":
            mode = "w"
        else:
            mode = "a"
        sortie = args[len(args) - 1]
        msg = arguments[
            0 : len(arguments)
            - len(args[len(args) - 2])
            - len(args[len(args) - 1])
            - 2
        ]
        # print(msg)

    try:
        if sortie == "stdout":
            print(arguments.replace("\\n", "\n"))
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
        print(e)


# list


def list(arguments: list):
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


def man(arguments: list):
    """\x1b[1mNAME:\x1b[0m
    man - display help

\x1b[1mSYNOPSIS:\x1b[0m
    \x1b[1mman\x1b[0m COMMAND

\x1b[1mDESCRIPTION:\x1b[0m
    display the help of the command
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "cmd", type=str, action="store", default="man", nargs="?"
    )
    args = parser.parse_args(arguments.split())
    print(COMMANDS.get(args.cmd, unknown_cmd).__doc__)


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


# main


def main():
    while True:
        inp = input(
            "\x1b[38:5:12m" + WORKING_DIRECTORY + "\x1b[38:5:208m $ \x1b[39m"
        )
        cmd = inp.split()
        if cmd[0] == "exit":
            exit()
            break
        COMMANDS.get(cmd[0], unknown_cmd)(inp[len(cmd[0]) + 1 :])


#

if __name__ == "__main__":
    main()
