import csv
import pandas as pd
import numpy as np
import argparse
from scipy.signal import find_peaks, butter, filtfilt
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style as PTStyle
from colorama import init, Fore, Style as CStyle
import sys

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
              You need to run this CLI in a folder where you have a CSV file exported from Physics Toolbox.
              Use Linear Accelerometer from Physics Toolbox, put your phone in your front pocket and start walking for a while.
              Don't forget to start recording! That's how you make your data!
              If you want to exit just type <exit> anytime
              
              """)

    found = False
    showed = False

    while True:
        if not found:
            message = prompt(
                [("class:prompt", "please enter the name of your CSV file>>> ")],
                style=style,
                completer=command_completer,
            ).strip()

        if message == "exit":
            exit_cli()


        file = find_file(message)
        if file is None: print("File not found")
        else:
            found = True

        if found and not showed:

            try:
               df_full = pd.read_csv(file, skiprows=3)

            except:
                found = False
                print("invalid CSV file")

            if "time" in df_full.columns and "ax (m/s^2)" in df_full.columns and "ay (m/s^2)" in df_full.columns and "az (m/s^2)" in df_full.columns and "aT (m/s^2)" in df_full.columns:
                seconds = df_full["time"].tolist()
                total_magnitude = df_full["aT (m/s^2)"].tolist()

                height_input = prompt([("class:prompt", "Enter user height in meters (e.g., 1.75)>>> ")],style=style).strip()

                if height_input == "exit":
                    exit_cli()

                try:
                    user_height = float(height_input)
                except ValueError:
                    print("Invalid height")
                    invalid = True

                if not invalid:
                    results = calculate_gait_metrics(total_magnitude, seconds, user_height)

                    print(f"\n{CStyle.BRIGHT}{Fore.CYAN}--- GAIT ANALYSIS REPORT ---{CStyle.RESET_ALL}")
                    for key, value in results.items():
                        print(f"{Fore.GREEN}{key}:{CStyle.RESET_ALL} {value}")
                    print(f"{CStyle.BRIGHT}{Fore.CYAN}----------------------------{CStyle.RESET_ALL}\n")

                    showed = True
                    exit_cli()

                found = False

            else:
                found = False
                print("invalid CSV file")





def find_file(filename):
    if os.path.exists(filename):
        return os.path.abspath(filename)
    else:
        return None


def calculate_gait_metrics(total_magnitude, seconds, height_m):
    aT = np.array(total_magnitude)
    t = np.array(seconds)

    b, a = butter(4, 3 / 50, btype='low')
    filtered_aT = filtfilt(b, a, aT)

    mean_aT = np.mean(filtered_aT)
    height_threshold = mean_aT * 1.1
    distance_threshold = 40

    peaks, _ = find_peaks(filtered_aT, height=height_threshold, distance=distance_threshold)

    total_steps = len(peaks)
    total_time_minutes = (t[-1] - t[0]) / 60.0
    cadence = total_steps / total_time_minutes if total_time_minutes > 0 else 0

    step_length = height_m * 0.415

    peak_values = filtered_aT[peaks]
    even_peaks = peak_values[::2]
    odd_peaks = peak_values[1::2]

    mean_even = np.mean(even_peaks) if len(even_peaks) > 0 else 0
    mean_odd = np.mean(odd_peaks) if len(odd_peaks) > 0 else 0

    symmetry = mean_even / mean_odd if mean_odd > 0 else 0

    return {
        "Total Steps": total_steps,
        "Cadence (steps/min)": round(cadence, 2),
        "Step Length (m)": round(step_length, 2),
        "Symmetry Ratio": round(symmetry, 3)
    }

def exit_cli():
    print("\nExiting program... Goodbye!")
    sys.exit(0)

