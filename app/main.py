import sys


def main():

    while True:
     sys.stdout.write("$ ")

     command = input()

     match command.split():
         case ["exit", "0"]:
             exit()
         case ["type", "echo"]:
             print("echo is a shell builtin")
         case ["type", "exit"]:
             print("exit is a shell builtin")
         case ["type", "type"]:
             print("type is a shell builtin")
         case ["type", arg]:
             print(f"{arg}: not found")
         case _:
             print(f"{command.split()[0]}: command not found")


if __name__ == "__main__":
    main()
