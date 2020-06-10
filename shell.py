#!usr/bin/env python3

import argparse
import fs
import sys
import os
import os.path as osp
import vixxd

sys.path.insert(
    0, osp.abspath(osp.join(osp.dirname(osp.abspath(__file__)), "ressource"))
)
import screen

FILE = ""
WORKING_DIRECTORY = "/"

# docstring parameter


def docstring_parameter(*sub):
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*sub)
        return obj

    return dec


# unknown command


@docstring_parameter(screen.BOLD, screen.DEFAULT)
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
    try:
        dir = fs.ls(PATH)
        for x in dir:
            if x[0] == file.encode():
                return int(x[2].decode())
        return -1
    except Exception:
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


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def ls(arguments: list):
    """{0}NAME:{1}
    ls - list directory contents

{0}SYNOPSIS:{1}
    {0}ls{1} [FILE] [OPTION]

{0}DESCRIPTION:{1}
    List  information  about the FILEs (the current directory by default)

    Mandatory arguments to long options are mandatory for short options too.

    {0}-l --long{1}
        print more informations.

    {0}-d --debug{1}
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
            print(screen.GREEN + " empty dir" + screen.DEFAULT)
        new_list = []
        for x in dir_content:
            new_list.append([int(x[2].decode()), x[0], x[1]])
        new_new_list = sorted(new_list)
        for x in new_new_list:
            if len(x) == 3:
                dir_size = size(dir, x[1].decode()) * 512
                if x[1].decode()[0] != "." or args.all == True:
                    print(
                        screen.GREEN
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
                        + screen.DEFAULT
                    )
    except SyntaxError as e:
        print(e)


# pwd command:


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def pwd(argument: list):
    """{0}NAME:{1}
    pwd - print name of current/working directory

{0}SYNOPSIS:{1}
    {0}pwd{1}

{0}DESCRIPTION:{1}
    Print the full filename of the current working directory.
    """
    print(WORKING_DIRECTORY)


# cd command:


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def cd(arguments: list):
    """{0}NAME:{1}
    cd - change working directory

{0}SYNOPSIS:{1}
    {0}cd{1} [FILE]

{0}DESCRIPTION:{1}
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


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def mkdir(arguments: list):  # PATH: str, name: str):
    """{0}NAME:{1}
    mkdir - make directories

{0}SYNOPSIS:{1}
    {0}mkdir{1} DIRECTORY

{0}DESCRIPTION:{1}
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


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def rmdir(arguments: list):
    """{0}NAME:{1}
    rmdir - remove empty directories

{0}SYNOPSIS:{1}
    {0}rmdir{1} DIRECTORY

{0}DESCRIPTION:{1}
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


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def touch(arguments: list):
    """{0}NAME:{1}
    touch - change file timestamps

{0}SYNOPSIS:{1}
    {0}touch{1} FILE

{0}DESCRIPTION:{1}
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


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def cp(arguments: list):
    """{0}NAME:{1}
    cp - copy files and directories

{0}SYNOPSIS:{1}
    {0}cp{1} SOURCE DEST

{0}DESCRIPTION:{1}
    Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.
    """
    parser = argparse.ArgumentParser()
    # parser.add_argument("-s", "--secure", action="store_true", default="False")
    parser.add_argument(
        "path1", type=str, action="store", default="", nargs="?"
    )
    parser.add_argument(
        "file1", type=str, action="store", default="", nargs="?"
    )
    parser.add_argument(
        "path2", type=str, action="store", default="", nargs="?"
    )
    parser.add_argument(
        "file2", type=str, action="store", default="", nargs="?"
    )
    args = parser.parse_args(arguments.split())
    # print(args)

    if args.file1 == "":
        print("error")
        return
    if (
        args.path1 != ""
        and args.file1 != ""
        and args.path2 == ""
        and args.file2 == ""
    ):
        PATH1 = WORKING_DIRECTORY
        PATH2 = WORKING_DIRECTORY
        file1 = args.path1
        file2 = args.file1
    elif (
        args.path1 != ""
        and args.file1 != ""
        and args.path2 != ""
        and args.file2 != ""
    ):
        PATH1 = args.path1
        PATH2 = args.path2
        file1 = args.file1
        file2 = args.file2
    elif args.file2 == "" and file_exist(args.path1, args.file1) == 1:
        PATH1 = args.path1
        file1 = args.file1
        PATH2 = WORKING_DIRECTORY
        file2 = args.path2
    elif args.file2 == "" and file_exist(args.file1, args.path2) == 1:
        PATH1 = WORKING_DIRECTORY
        file1 = args.path1
        PATH2 = args.file1
        file2 = args.path2
    if PATH1[0] != "/":
        PATH1 = WORKING_DIRECTORY + PATH1
    if PATH1[-1] != "/":
        PATH1 += "/"
    if PATH2[0] != "/":
        PATH2 = WORKING_DIRECTORY + PATH2
    if PATH2[-1] != "/":
        PATH2 += "/"
    if not file_exist(PATH1, file1) == 1 and not file_exist(PATH2, file2) == 1:
        pass
    print(PATH1, file1, PATH2, file2)
    try:
        filea1 = fs.fopen(PATH1 + file1, "r")
        filea2 = fs.fopen(PATH2 + file2, "w")
    except Exception:
        print("error")
        return
    content = filea1.fread()
    filea2.fwrite(content)
    print("done")


# rm


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def rm(arguments: list):  # PATH: str, file: str, mode=0):
    """{0}NAME:{1}
    rm - remove files

{0}SYNOPSIS:{1}
    {0}rm{1} FILE

{0}DESCRIPTION:{1}
    removes specified file.

    Mandatory arguments to long options are mandatory for short options too.

    {0}-s --secure{1}
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


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def mv(arguments: list):
    """{0}NAME:{1}
    mv - move (rename) files

{0}SYNOPSIS:{1}
    {0}mv{1} SOURCE DEST

{0}DESCRIPTION:{1}
    Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY.
    """
    parser = argparse.ArgumentParser()
    # parser.add_argument("-s", "--secure", action="store_true", default="False")
    parser.add_argument(
        "path1", type=str, action="store", default="", nargs="?"
    )
    parser.add_argument(
        "file1", type=str, action="store", default="", nargs="?"
    )
    parser.add_argument(
        "path2", type=str, action="store", default="", nargs="?"
    )
    parser.add_argument(
        "file2", type=str, action="store", default="", nargs="?"
    )
    args = parser.parse_args(arguments.split())
    # print(args)

    if args.file1 == "":
        print("error")
        return
    if (
        args.path1 != ""
        and args.file1 != ""
        and args.path2 == ""
        and args.file2 == ""
    ):
        PATH1 = WORKING_DIRECTORY
        PATH2 = WORKING_DIRECTORY
        file1 = args.path1
        file2 = args.file1
    elif (
        args.path1 != ""
        and args.file1 != ""
        and args.path2 != ""
        and args.file2 != ""
    ):
        PATH1 = args.path1
        PATH2 = args.path2
        file1 = args.file1
        file2 = args.file2
    elif args.file2 == "" and file_exist(args.path1, args.file1) == 1:
        PATH1 = args.path1
        file1 = args.file1
        PATH2 = WORKING_DIRECTORY
        file2 = args.path2
    elif args.file2 == "" and file_exist(args.file1, args.path2) == 1:
        PATH1 = WORKING_DIRECTORY
        file1 = args.path1
        PATH2 = args.file1
        file2 = args.path2
    if PATH1[0] != "/":
        PATH1 = WORKING_DIRECTORY + PATH1
    if PATH1[-1] != "/":
        PATH1 += "/"
    if PATH2[0] != "/":
        PATH2 = WORKING_DIRECTORY + PATH2
    if PATH2[-1] != "/":
        PATH2 += "/"
    if not file_exist(PATH1, file1) == 1 and not file_exist(PATH2, file2) == 1:
        pass
    print(PATH1, file1, PATH2, file2)
    try:
        filea1 = fs.fopen(PATH1 + file1, "r")
        filea2 = fs.fopen(PATH2 + file2, "w")
    except Exception:
        print("error")
        return
    content = filea1.fread()
    filea2.fwrite(content)
    fs.rm(PATH1, file1)
    print("done")


# cat


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def cat(arguments: list):
    """{0}NAME:{1}
    cat - print the file content on the standard output

{0}SYNOPSIS:{1}
    {0}cat{1} FILE

{0}DESCRIPTION:{1}
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
    if PATH[0] != "/":
        PATH = WORKING_DIRECTORY + PATH
    if PATH[-1] != "/":
        PATH += "/"
    if not file_exist(PATH, file) == 1:
        print("fichier inexistant")
        return
    files = [x[0] for x in fs.ls(PATH)]
    if file.encode() not in files:
        print("fichier inexistant")
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


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def tac(arguments: list):
    """{0}NAME:{1}
    cat - print the file content on the standard output in reverse

{0}SYNOPSIS:{1}
    {0}tac{1} FILE

{0}DESCRIPTION:{1}
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
    if PATH[0] != "/":
        PATH = WORKING_DIRECTORY + PATH
    if PATH[-1] != "/":
        PATH += "/"
    if not file_exist(PATH, file) == 1:
        print("fichier inexistant")
        return
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


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def head(arguments: list):
    """{0}NAME:{1}
    head - output the first part of files

{0}SYNOPSIS:{1}
    {0}head{1} FILE

{0}DESCRIPTION:{1}
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
    if PATH[0] != "/":
        PATH = WORKING_DIRECTORY + PATH
    if PATH[-1] != "/":
        PATH += "/"
    if not file_exist(PATH, file) == 1:
        print("fichier inexistant")
        return
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


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def tail(arguments: list):
    """{0}NAME:{1}
    tail - output the last part of files

{0}SYNOPSIS:{1}
    {0}tail{1} FILE

{0}DESCRIPTION:{1}
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
    if PATH[0] != "/":
        PATH = WORKING_DIRECTORY + PATH
    if PATH[-1] != "/":
        PATH += "/"
    if not file_exist(PATH, file) == 1:
        print("fichier inexistant")
        return
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


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def echo(arguments: str):  # msg: str, sortie: str = "stdout", mode="w"):
    """{0}NAME:{1}
    echo - display a line of text

{0}SYNOPSIS:{1}
    {0}echo{1} STRING

{0}DESCRIPTION:{1}
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


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def list(arguments: list):
    """{0}NAME:{1}
    list - list all commands

{0}SYNOPSIS:{1}
    {0}list{1}

{0}DESCRIPTION:{1}
    display the list of all commands
    """
    for x in COMMANDS.keys():
        print(screen.GREEN + x + screen.DEFAULT)


# man


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def man(arguments: list):
    """{0}NAME:{1}
    man - display help

{0}SYNOPSIS:{1}
    {0}man{1} COMMAND

{0}DESCRIPTION:{1}
    display the help of the command
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "cmd", type=str, action="store", default="man", nargs="?"
    )
    args = parser.parse_args(arguments.split())
    print(COMMANDS.get(args.cmd, unknown_cmd).__doc__)


# exit


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def exit():
    """{0}NAME:{1}
    exit - exit shell

{0}SYNOPSIS:{1}
    {0}exit{1}

{0}DESCRIPTION:{1}
    exit the shell
    """
    pass


@docstring_parameter(screen.BOLD, screen.DEFAULT)
def xxd(arguments: list):
    """
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
    if PATH[0] != "/":
        PATH = WORKING_DIRECTORY + PATH
    if PATH[-1] != "/":
        PATH += "/"
    if not file_exist(PATH, file) == 1:
        print("fichier inexistant")
        return
    files = [x[0] for x in fs.ls(PATH)]
    if file.encode() not in files:
        print("fichier non existant")
        return
    try:
        print(vixxd.main(PATH + "/" + file))
    except SyntaxError as e:
        print(e)
        return


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
    "xxd": xxd,
}


# main


def main(file=FILE):
    FILE = file
    while True:
        inp = input(
            screen.BLUE
            + WORKING_DIRECTORY
            + screen.ORANGE
            + " $ "
            + screen.DEFAULT
        )
        cmd = inp.split()
        if cmd[0] == "exit":
            exit()
            break
        COMMANDS.get(cmd[0], unknown_cmd)(inp[len(cmd[0]) + 1 :])


#

if __name__ == "__main__":
    fs.open(FILE)
    main()
