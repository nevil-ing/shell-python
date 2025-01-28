import readline
import sys
import os
import subprocess
import shlex
from sys import executable


def executables():
    """Return a list of all executable files in the PATH."""
    executables = []
    paths = os.getenv("PATH").split(":")
    for path in paths:
        if os.path.isdir(path):
            executables.extend(
                [
                    f
                    for f in os.listdir(path)
                    if os.access(os.path.join(path, f), os.X_OK)
                ]
            )
    return executables


def completer(text, state):
    """Auto-complete function for built-in commands and executables."""
    builtin = ["echo ", "type ", "pwd ", "cd ", "exit "]
    matches = [cmd for cmd in builtin + executables() if cmd.startswith(text)]

    if not matches:
        return None

    if state < len(matches):
        return matches[state]
    else:
        return None


def display_matches(text):
    """Display the matches when tab is pressed twice."""
    builtin = ["echo ", "type ", "pwd ", "cd ", "exit "]
    matches = [cmd for cmd in builtin + executables() if cmd.startswith(text)]
    if matches:
        # Print the matches separated by 2 spaces
        sys.stdout.write("\r")  # Move cursor to the beginning of the line
        sys.stdout.write("  ".join(matches) + "\n")  # Print matches and move to a new line
        # Print the prompt with the current text
        sys.stdout.write("$ " + text)  # Print the prompt without a newline
        sys.stdout.flush()


def main():
    PATH = os.environ.get("PATH")

    BUILTINS = {
        "echo": "echo is a shell builtin",
        "exit": "exit is a shell builtin",
        "type": "type is a shell builtin",
        "pwd": "pwd is a shell builtin",
        "cd": "cd is a shell builtin",
    }

    last_tab_pressed = {"count": 0, "last_text": ""}

    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

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
                stdout_mode = "w"  # Set write mode for >
            elif token == "1>":
                stdout_file = next(iterator)
                stdout_mode = "w"  # Set write mode for 1>
            elif token == ">>":
                stdout_file = next(iterator)
                stdout_mode = "a"  # Set append mode for >>
            elif token == "1>>":
                stdout_file = next(iterator)
                stdout_mode = "a"  # Set append mode for 1>>
            elif token == "2>":
                stderr_file = next(iterator)
                stderr_mode = "w"  # Set write mode for 2>
            elif token == "2>>":
                stderr_file = next(iterator)
                stderr_mode = "a"  # Set append mode for 2>>
            else:
                command.append(token)
        return command, stdout_file, stderr_file, stdout_mode, stderr_mode

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()

        if command and command[-1] == "\t":
            command = command[:-1]  # Remove the TAB character
            if last_tab_pressed["last_text"] == command:
                last_tab_pressed["count"] += 1
            else:
                last_tab_pressed = {"count": 1, "last_text": command}

            if last_tab_pressed["count"] == 1:
                # Ring the bell on the first TAB press
                sys.stdout.write("\a")
                sys.stdout.flush()

            if last_tab_pressed["count"] == 2:
                # Display matches on the second TAB press
                display_matches(command)
                last_tab_pressed["count"] = 0
                continue  # Continue so the main loop will start from the prompt again
            else:
                continue

        if not command.strip():
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
                command_to_execute, stdout_file, stderr_file, stdout_mode, stderr_mode = handle_redirection(
                    parsed_command)
                if stdout_file or stderr_file:
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
                        except subprocess.CalledProcessError:
                            pass  # Do not print error to stdout. Just continue prompt.
                    else:
                        print(f"{cmd_name}: command not found")
                else:
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
                    cms_dis_name = os.path.basename(executable)
                    try:
                        stdout = open(stdout_file, stdout_mode) if stdout_file else None
                        stderr = open(stderr_file, stderr_mode) if stderr_file else None

                        subprocess.run([cms_dis_name, *cmd_args], stdout=stdout, stderr=stderr, check=True)

                        if stdout:
                            stdout.close()
                        if stderr:
                            stderr.close()
                    except FileNotFoundError:
                        print(f"{cmd_name}: command not found")
                    except subprocess.CalledProcessError:
                        pass
                else:
                    print(f"{cmd_name}: command not found")


if __name__ == "__main__":
    main()