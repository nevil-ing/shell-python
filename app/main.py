import sys
import os
import subprocess
import shlex

def main():
    PATH = os.environ.get("PATH")


    BUILTINS = {
        "echo": "echo is a shell builtin",
        "exit": "exit is a shell builtin",
        "type": "type is a shell builtin",
        "pwd" : "pwd is a shell builtin",
        "cd" : "cd is a shell builtin"
    }
    def shell_echo_commands(arguments):
        for i in range(len(arguments)):
            if (arguments[i].startswith("'") and arguments[i].endswith("'")) or (arguments[i].startswith('"') and arguments[i].endswith('"')):
                arguments[i] = arguments[i][1:-1]
        print(" ".join(arguments))


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
            # print(*args)
             shell_echo_commands(args)
         case ["pwd"]:
            print(os.getcwd())
         case ["cd", "~"]:
             home_dir = os.path.expanduser("~")
             os.chdir(home_dir)
         case ["cd", args]:
             new_dir = args
             try:
                os.chdir(new_dir)
             except FileNotFoundError:
                 print(f"cd: {new_dir}: No such file or directory")

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
