import pandas as pd
import numpy as np
import argparse
from scipy.signal import find_peaks, butter, filtfilt
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style as PTStyle
from colorama import init, Fore, Style as CStyle

style = PTStyle.from_dict({
    "prompt": "ansigreen dim",
    "": "bold ansibrightgreen",
})

current_folder = os.getcwd()
all_items = os.listdir(current_folder)
file = None
files = [f for f in all_items if os.path.isfile(os.path.join(current_folder, f)) and f.endswith(".csv")]
commnads = files
command_completer = WordCompleter(commnads, ignore_case=True)


def main():
    print(fr"""{CStyle.BRIGHT} {Fore.YELLOW}
         ________         __ __     __                   _______               __                         
        |  |  |  |.---.-.|  |  |--.|__|.-----.-----.    |   _   |.-----.---.-.|  |.--.--.-----.-----.----.
        |  |  |  ||  _  ||  |    < |  ||     |  _  |    |       ||     |  _  ||  ||  |  |-- __|  -__|   _|
        |________||___._||__|__|__||__||__|__|___  |    |___|___||__|__|___._||__||___  |_____|_____|__|  
                                             |_____|                              |_____|                    
                                             
              Welcome to my CLI project. Here you can calculate step length, cadence, and symmetry.
              Type 'help' to see available commands or read more information.{CStyle.RESET_ALL}
              """)

    while True:
        message = prompt(
            [("class:prompt", "please enter the name of your CSV file>>> ")],
            style=style,
            completer=command_completer,
        ).strip()

        file = find_file(message)
        if file is None: print("File not found")



def find_file(filename):
    if os.path.exists(filename):
        return open(filename, "rb")
    else:
        return None