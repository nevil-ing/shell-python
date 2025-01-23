import sys
import os
import subprocess

def main():
    PATH = os.environ.get("PATH")

    BUILTINS = {
        "echo": "echo is a shell builtin",
        "exit": "exit is a shell builtin",
        "type": "type is a shell builtin",
        "pwd" : "pwd is a shell builtin"
    }
    while True:
     sys.stdout.write("$ ")
     sys.stdout.flush()
     command = input()

     match command.split():
         case ["exit", "0"]:
             exit()
         case ["type", cmd] if cmd in BUILTINS:
             print(BUILTINS[cmd])
         case ["type", cmd]:

             cmd_path = None
             paths = os.environ.get("PATH", "").split(os.pathsep)
             for path in paths:
                 if os.path.isfile(f"{path}/{cmd}"):
                     cmd_path = f"{path}/{cmd}"
             if cmd_path:
                 print(f"{cmd} is {cmd_path}")
             else:
                 print(f"{cmd}: not found")
         case ["echo", *args]:
             print(*args)
         case ["pwd"]:
            print(os.getcwd())

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

                 cmd_dis_name = os.path.basename(executable)
                 try:
                     subprocess.run([cmd_dis_name, *cmd_args], check=True)
                 except subprocess.CalledProcessError as e:
                     print(f"Error while executing {cmd_name}: {e}")
             else:
                 print(f"{cmd_name}: command not found")

if __name__ == "__main__":
    main()
