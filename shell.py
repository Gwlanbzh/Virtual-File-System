import fs
WORKING_DIRECTORY = "/"

# ls command

def ls_command(dir: str):
    if dir == "":
        dir = WORKING_DIRECTORY
    dir_content = fs.ls(dir)
    for x in dir_content:
        print(" " + x[0].decode())
    print("")

# cd command:

def cd(dir: str):
    global WORKING_DIRECTORY
    if dir == "":
        WORKING_DIRECTORY = "/"
    else:
        if WORKING_DIRECTORY == "/":
            if dir[len(dir) - 1] != "/":
                WORKING_DIRECTORY += dir + "/"
            else:
                WORKING_DIRECTORY += dir
        else:
            if dir[len(dir) - 1] != "/":
                WORKING_DIRECTORY += "/" + dir + "/"
            else:
                WORKING_DIRECTORY += "/" + dir

# main

def main():
    while True:
        inp = input(WORKING_DIRECTORY + " $ ")
        if inp[0:2] == "ls":
            ls_command(inp[2:len(inp)])
        elif inp[0:2] == "cd":
            cd(inp[2:len(inp)].replace(" ", ""))
        elif "exit" in inp:
            break
        else:
            print("error")

#


main()
