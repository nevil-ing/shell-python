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
      print(" ".join(arguments))

    def handle_redirection(parsed_command):
        stdout_file = None
        stderr_file = None
        stdout_mode = "w"
        stderr_mode = "w"

        command = []
        iterator = iter(parsed_command)
        for token in iterator:
            if token == ">":
                stdout_file = next(iterator)
            elif token == ">>":
                stdout_file = next(iterator)
                stdout_mode = "a"
            elif token == "2>":
                stderr_file = next(iterator)
            elif token == "2>>":
                stderr_file = next(iterator)
                stderr_mode = "a"
            else:
                command.append(token)
        return command, stdout_file, stderr_file,stdout_mode, stderr_mode


    while True:
     sys.stdout.write("$ ")
     sys.stdout.flush()
     command = input()
     parsed_command = shlex.split(command)

     match parsed_command:
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
             cmd_name = parsed_command[0]
             cmd_args = parsed_command[1:]

             cmd_args, stdout_file, stderr_file,stdout_mode, stderr_mode = handle_redirection(parsed_command)

             executable = None
             for path in os.environ.get("PATH", "").split(os.pathsep):
                 potential_executable = os.path.join(path, cmd_name)
                 if os.path.isfile(potential_executable) and os.access(potential_executable, os.X_OK):
                     executable = potential_executable
                     break

             if executable:

                 if ">" in parsed_command or ">>" in parsed_command:
                     try:
                         # Check for redirection operators
                         if ">>" in parsed_command:
                             operator_index = parsed_command.index(">>")
                             mode = "a"  # Append mode
                         else:
                             operator_index = parsed_command.index(">")
                             mode = "w"  # Overwrite mode

                         # Extract the output file path and command
                         output_file = parsed_command[operator_index + 1]
                         command_to_run = parsed_command[:operator_index]

                         # Open the file and redirect stdout
                         with open(output_file, mode) as outfile:
                             subprocess.run(command_to_run, stdout=outfile, stderr=subprocess.PIPE, check=True)

                     except FileNotFoundError as e:
                         print(f"Error: {e}")
                     except subprocess.CalledProcessError as e:
                         print(f"Error while executing command: {e}")
                 else:
                     # Normal command execution without redirection
                     try:
                         subprocess.run(parsed_command, check=True)
                     except subprocess.CalledProcessError as e:
                         print(f"Error while executing command: {e}")


             else:
                 print(f"{cmd_name}: command not found")
if __name__ == "__main__":
    main()
