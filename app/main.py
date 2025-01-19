import sys


def main():

    while True:
     sys.stdout.write("$ ")

     command = input()
     if command == "exit 0":
          sys.exit(0)
     command.startswith("echo")
     output = command.lstrip('echo')

     print(f"{output.strip()}")

     #print(f"{command}: command not found")






if __name__ == "__main__":
    main()
