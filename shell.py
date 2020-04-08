import fs

WORKING_DIRECTORY = "/"

# ls command


def ls(dir: str):
    if dir == "":
        dir = WORKING_DIRECTORY
    dir_content = fs.ls(dir)
    for x in dir_content:
        if int(x[2].decode()) == 0:
            print(" " + x[0].decode() + "/")
        else:
            print(" " + x[0].decode())


# pwd command:


def pwd():
    print(WORKING_DIRECTORY)


# cd command:


def cd(dir: str):
    global WORKING_DIRECTORY
    if dir == "":
        WORKING_DIRECTORY = "/"
    elif dir[0] != "/":
        if dir[len(dir) - 1] != "/":
            WORKING_DIRECTORY += dir + "/"
        else:
            WORKING_DIRECTORY += dir
    else:
        if dir[len(dir) - 1] != "/":
            WORKING_DIRECTORY = dir + "/"
        else:
            WORKING_DIRECTORY = dir


# mkdir


def mkdir(PATH: str, name: str):
    dir = fs.mkdir(PATH, name)
    if dir == 0:
        print("directory {} sucessfully created".format(PATH + "/" + name))
    else:
        print("error")


# rmdir


def rmdir(PATH: str, name: str):
    dir = fs.rmdir(PATH, name)
    if dir == 0:
        print("directory {} sucessfully remove".format(PATH + "/" + name))
    else:
        print("error")


# touch


def touch(PATH: str, name: str):
    pass


# cp


def cp(file: str, PATH: str):
    pass


# rm


def rm(PATH: str, file: str):
    pass


# mv


def mv(file: str, file: str):
    pass


# cat


def cat(file: str):
    pass


# tac


def tac(file: str):
    pass


# head


def head(file: str):
    pass


# tail


def tail(file: str):
    pass


# man


def man(cmd: str):
    pass


# echo


def echo(msg: str, file=""):
    pass


# main


def main():
    while True:
        inp = input(WORKING_DIRECTORY + " $ ")
        cmd = inp.split()
        if cmd[0] == "ls":
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
        elif cmd[0] == "exit":
            break
        else:
            print("error")


#


main()
