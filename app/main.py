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

             cmd_parts = command.split()
             cmd_name = cmd_parts[0]
             cmd_args = cmd_parts[1:]

             executable = None
             for path in os.environ.get("PATH", "").split(os.pathsep):
                 potential_executable = os.path.join(path, cmd_name)
                 if os.path.isfile(potential_executable) and os.access(potential_executable, os.X_OK):
                     executable = potential_executable
                     break

             if executable:


                os.execvp(executable, [cmd_name, *cmd_args])

             else:
                 print(f"{cmd_name}: command not found")


if __name__ == "__main__":
    main()
