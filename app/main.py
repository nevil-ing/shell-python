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
        "pwd": "pwd is a shell builtin",
        "cd": "cd is a shell builtin",
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
            elif token == "1>":
                stdout_file = next(iterator)
                stdout_mode = "a"
            elif token == "2>":
                stderr_file = next(iterator)
            elif token == "2>>":
                stderr_file = next(iterator)
                stderr_mode = "a"
            else:
                command.append(token)
        return command, stdout_file, stderr_file, stdout_mode, stderr_mode

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input().strip()
        if not command:
            continue

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
                        break
                if cmd_path:
                    print(f"{cmd} is {cmd_path}")
                else:
                    print(f"{cmd}: not found")
            case ["echo", *args]:
                # Special case for 'echo' with possible redirection handled here
                command_to_execute, stdout_file, stderr_file, stdout_mode, stderr_mode = handle_redirection(
                    parsed_command)
                if stdout_file or stderr_file:  # If there is a redirection on echo, use subprocess.run
                    cmd_name = command_to_execute[0]
                    cmd_args = command_to_execute[1:]

                    executable = None
                    for path in os.environ.get("PATH", "").split(os.pathsep):
                        potential_executable = os.path.join(path, cmd_name)
                        if os.path.isfile(potential_executable) and os.access(potential_executable, os.X_OK):
                            executable = potential_executable
                            break

                    if executable:
                        try:
                            stdout = open(stdout_file, stdout_mode) if stdout_file else None
                            stderr = open(stderr_file, stderr_mode) if stderr_file else None

                            subprocess.run([executable, *cmd_args], stdout=stdout, stderr=stderr, check=True)

                            if stdout:
                                stdout.close()
                            if stderr:
                                stderr.close()
                        except FileNotFoundError:
                            print(f"{cmd_name}: command not found")
                        except subprocess.CalledProcessError as e:
                            print(f"Command execution failed: {e}")
                    else:
                        print(f"{cmd_name}: command not found")
                else:  # if there is no redirection, we can use the shell_echo_commands.
                    shell_echo_commands(args)
            case ["pwd"]:
                print(os.getcwd())
            case ["cd", "~"]:
                home_dir = os.path.expanduser("~")
                os.chdir(home_dir)
            case ["cd", directory]:
                try:
                    os.chdir(directory)
                except FileNotFoundError:
                    print(f"cd: {directory}: No such file or directory")
            case _:
                command_to_execute, stdout_file, stderr_file, stdout_mode, stderr_mode = handle_redirection(
                    parsed_command)
                cmd_name = command_to_execute[0]
                cmd_args = command_to_execute[1:]

                executable = None
                for path in os.environ.get("PATH", "").split(os.pathsep):
                    potential_executable = os.path.join(path, cmd_name)
                    if os.path.isfile(potential_executable) and os.access(potential_executable, os.X_OK):
                        executable = potential_executable
                        break

                if executable:
                    try:
                        stdout = open(stdout_file, stdout_mode) if stdout_file else None
                        stderr = open(stderr_file, stderr_mode) if stderr_file else None

                        subprocess.run([executable, *cmd_args], stdout=stdout, stderr=stderr, check=True)

                        if stdout:
                            stdout.close()
                        if stderr:
                            stderr.close()
                    except FileNotFoundError:
                        print(f"{cmd_name}: command not found")
                    except subprocess.CalledProcessError as e:
                        print(f"Command execution failed: {e}")
                else:
                    print(f"{cmd_name}: command not found")


if __name__ == "__main__":
    main()