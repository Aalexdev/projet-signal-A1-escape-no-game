import numpy as np
import sounddevice as sd
from matplotlib import pyplot as plt

import program
import commands
import variables

# All the registred commands and their functions


def main():
    while True:
        # Get the user command
        user_input = input("enter command : ").split()

        # Check if user_input is empty
        if not user_input:
            continue
        
        # Checks if the command is registred
        if not user_input[0] in commands.cmds:
            print(f"\"{user_input[0]}\" is not a registred command")
            continue
        
        # Calls the command
        func = commands.cmds.get(user_input[0])

        result = func(user_input[1:])

        if result == commands.Status.EXIT:
            print("EXIT")
            break

        elif result == commands.Status.INVALID_ARGS:
            print(f"Invalid arguments for \"{user_input[0]}\"")
        
        elif result == commands.Status.FAILURE:
            print("FAILURE")

if __name__ == "__main__":
    main()