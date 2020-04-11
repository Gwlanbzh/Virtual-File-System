#!usr/bin/python3.6

import fs

WORKING_DIRECTORY = "/"
COMMANDS = {
    "ls": "liste les fichiers dans un répertoire",
    "cd": "permet de se déplacer dans l'arborescence",
    "pwd": "affiche le répertoire de travaille",
    "mkdir": "créé un répertoire vide",
    "rmdir": "supprime un répertoire",
    "touch": "créé un fichier vide",
    "cp": "copie un fichier",
    "rm": "supprime un fichier",
    "mv": "déplace un fichier",
    "cat": "lis le contenue d'un fichier",
    "tac": "lis le contenue d'un fichier de la fin au début",
    "head": "lis les premières lignes d'un fichier",
    "tail": "lis les dernières lignes d'un fichier",
    "man": "affiche l'aide",
    "echo": "écrit des caractères sur une sortie",
    "exit": "quitte le shell",
}
# ls command


def ls(dir: str, mode=""):
    """liste les fichiers dans un répertoire
    """
    try:
        if dir == "":
            dir = WORKING_DIRECTORY
        dir_content = fs.ls(dir)
        if dir_content == [[b""]]:
            print("\x1b[38:5:10m empty dir\x1b[39m")
        for x in dir_content:
            if len(x) == 3:
                if int(x[2].decode()) == 0:
                    if mode == "-d" or mode == "--debug":
                        print(
                            "\x1b[38:5:10m "
                            + x[0].decode()
                            + "/  "
                            + " " * (10 - len(x[0].decode()) - 1)
                            + str(x[1])
                            + "\x1b[39m"
                        )
                    elif mode == "-l":
                        print(
                            "\x1b[38:5:10m "
                            + x[0].decode()
                            + "/  "
                            + " " * (10 - len(x[0].decode()) - 1)
                            + str(len(x[1]) * 512)
                            + "\x1b[39m"
                        )
                    else:
                        print(
                            "\x1b[38:5:10m "
                            + x[0].decode()
                            + "/   "
                            + "\x1b[39m"
                        )
                else:
                    if mode == "-d" or mode == "--debug":
                        print(
                            "\x1b[38:5:10m "
                            + x[0].decode()
                            + "  "
                            + " " * (10 - len(x[0].decode()))
                            + str(x[1])
                            + "\x1b[39m"
                        )
                    elif mode == "-l":
                        print(
                            "\x1b[38:5:10m "
                            + x[0].decode()
                            + "  "
                            + " " * (10 - len(x[0].decode()))
                            + str(len(x[1]) * 512)
                            + "\x1b[39m"
                        )
                    else:
                        print("\x1b[38:5:10m " + x[0].decode() + " \x1b[39m")
            else:
                pass
    except SyntaxError as e:
        print(e)


# pwd command:


def pwd():
    """affiche le répertoire de travaille
    """
    print(WORKING_DIRECTORY)


# cd command:


def cd(dir: str):
    """permet de se déplacer dans l'arborescence
    """
    global WORKING_DIRECTORY
    if dir == "":
        WORKING_DIRECTORY = "/"
    elif dir[0] != "/":
        if dir[len(dir) - 1] != "/":
            data = dir.split("/")
            PATH = dir[0 : len(dir) - len(data[len(data) - 1])]
            if file_exist(WORKING_DIRECTORY + PATH, data[len(data) - 1]) != 0:
                print("dossier inexistant")
                return
            WORKING_DIRECTORY += dir + "/"
        else:
            data = dir.split("/")
            PATH = dir[0 : len(dir) - len(data[len(data) - 2]) - 1]
            if file_exist(WORKING_DIRECTORY + PATH, data[len(data) - 2]) != 0:
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


# mkdir


def mkdir(PATH: str, name: str):
    """créé un répertoire vide
    """
    dir = fs.mkdir(PATH, name)
    if dir == 0:
        print("directory {} sucessfully created".format(PATH + name))
    else:
        print("error")


# rmdir


def rmdir(PATH: str, name: str):
    """supprime un répertoire
    """
    dir = fs.rmdir(PATH, name)
    if dir == 0:
        print("directory {} sucessfully remove".format(PATH + name))
    else:
        print("invalid directory name or directory not empty")


# touch


def touch(PATH: str, name: str):
    """créé un fichier vide
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
    """copie un fichier
    """
    pass


# rm


def rm(PATH: str, file: str, mode=0):
    """supprime un fichier
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
    """déplace un fichier
    """
    pass


# cat


def cat(PATH: str, file: str):
    """lis le contenue d'un fichier
    """
    files = [x[0] for x in fs.ls(PATH)]
    if file.encode() not in files:
        print("fichier non existant")
        return
    try:
        file = fs.fopen(PATH + "/" + file, "r")
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
    """lis le contenue d'un fichier de la fin au début
    """
    files = [x[0] for x in fs.ls(PATH)]
    if file.encode() not in files:
        print("fichier non existant")
        return
    try:
        file = fs.fopen(PATH + "/" + file, "r")
        data = file.fread()
        file.fclose()
        for x in data.split("\\n"):
            print(x[::-1])
    except SyntaxError as e:
        print(e)
        return


# head


def head(PATH: str, file: str):
    """lis les premières lignes d'un fichier
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
    """lis les dernières lignes d'un fichier
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


# man


def man(cmd: str = "man"):
    """affiche l'aide
    """
    if cmd not in COMMANDS.keys():
        print("invalid argument")
    else:
        print(COMMANDS[cmd])


# echo


def echo(msg: str, sortie: str = "stdout"):
    """écrit des caractères sur une sortie
    """
    try:
        if sortie == "stdout":
            print(msg)
        else:
            if sortie[0] == "/":
                file = fs.fopen(sortie, "w")
                file.fwrite(msg)
                file.fclose()
            else:
                file = fs.fopen(WORKING_DIRECTORY + sortie, "w")
                file.fwrite(msg)
                file.fclose()
            print("sucess")
    except SyntaxError as e:
        print("le dossier n'existe pas")


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
            data = inp.split(">")
            if len(data) == 1:
                echo(data[0][5 : len(data[0])])
            elif len(data) == 2:
                echo(data[0][5 : len(data[0]) - 1], data[1][1 : len(data[1])])
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
        elif cmd[0] == "exit":
            break


#

if __name__ == "__main__":
    main()
