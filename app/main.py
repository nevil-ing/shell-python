import sys
import os

def main():
    PATH = os.environ.get("PATH")
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
             cmd = arg
             cmd_path = None
             paths = os.environ.get("PATH", "").split(os.pathsep)
             for path in paths:
                 if os.path.isfile(f"{path}/{cmd}"):
                     cmd_path = f"{path}/{cmd}"
             if cmd_path:
                 print(f"{cmd} is {cmd_path}")
             else:
                 print(f"{arg}: not found")
         case ["echo", *args]:
             print(*args)

         case _:

             if os.path.isfile(command.split()[0]):
                 os.system(command)
             else:
                 print(f"{command.split()[0]}: command not found")



if __name__ == "__main__":
    main()
