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


def ls(dir: str):
    """liste les fichiers dans un répertoire
    """
    try:
        if dir == "":
            dir = WORKING_DIRECTORY
        dir_content = fs.ls(dir)
        for x in dir_content:
            if int(x[2].decode()) == 0:
                print("\x1b[38:5:10m " + x[0].decode() + "/\x1b[39m")
            else:
                print("\x1b[38:5:10m " + x[0].decode() + "\x1b[39m")
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
            if file_exist(WORKING_DIRECTORY, dir) != 0:
                print("dossier inexistant")
                return
            WORKING_DIRECTORY += dir + "/"
        else:
            if file_exist(WORKING_DIRECTORY, dir[0 : len(dir) - 1]) != 0:
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
        print("directory {} sucessfully created".format(PATH + "/" + name))
    else:
        print("error")


# rmdir


def rmdir(PATH: str, name: str):
    """supprime un répertoire
    """
    dir = fs.rmdir(PATH, name)
    if dir == 0:
        print("directory {} sucessfully remove".format(PATH + "/" + name))
    else:
        print("error")


# touch


def touch(PATH: str, name: str):
    """créé un fichier vide
    """
    if name in fs.ls(PATH):
        print("fichier déjà existant")
        return
    file = fs.fopen(PATH + "/" + name, "w")
    file.fwrite("")
    file.fclose()
    print("fichier créé")


# cp


def cp(file: str, PATH: str):
    """copie un fichier
    """
    pass


# rm


def rm(PATH: str, file: str):
    """supprime un fichier
    """
    pass


# mv


def mv(file1: str, file2: str):
    """déplace un fichier
    """
    pass


# cat


def cat(PATH: str, file: str):
    """lis le contenue d'un fichier
    """
    if name not in fs.ls(PATH):
        print("fichier non existant")
        return
    file = fs.fopen(PATH + "/" + name, "r")
    data = file.fread()
    file.fclose()
    print(data)


# tac


def tac(PATH: str, file: str):
    """lis le contenue d'un fichier de la fin au début
    """
    pass


# head


def head(file: str):
    """lis les premières lignes d'un fichier
    """
    pass


# tail


def tail(file: str):
    """lis les dernières lignes d'un fichier
    """
    pass


# man


def man(cmd: str = "man"):
    """affiche l'aide
    """
    if cmd not in COMMANDS.keys():
        print("invalid argument")
    else:
        print(COMMANDS[cmd])


# echo


def echo(msg: str, file: str = "stdout"):
    """écrit des caractères sur une sortie
    """
    pass


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
        if cmd[0] not in COMMANDS.keys():
            print("invalide command")
        elif cmd[0] == "ls":
            if len(cmd) > 1:
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
        elif cmd[0] == "man":
            if len(cmd) > 1:
                man(cmd[1])
            else:
                man()
        elif cmd[0] == "exit":
            break


#

if __name__ == "__main__":
    main()
