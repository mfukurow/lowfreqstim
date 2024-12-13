"""
stim trigger App

send single trigger pulse to a function generator
and record the stimulus information in a csv file  

efish lab
Hokkaido University
Author: Matasaburo Fukutomi
Email: mfukurow@gmail.com
"""

from tdt import DSPCircuit, DSPError
import csv
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from tkinter.simpledialog import askstring
import time


def connect_RM1():
    try:
        circuit = DSPCircuit("lowfreqstim.rcx", "RM1", "USB")
        circuit.start()
        return circuit
    except DSPError as e:
        print("Error acquiring data: {}".format(e))
        messagebox.showerror("Error", "Failed to connect to RM1.")
        return None


def name_csv():
    folderpath = askdirectory(title="Choose Directory")
    if not folderpath:
        messagebox.showerror("Error", "No directory selected!")
        return None
    filename = askstring("CSV file name", "Enter file name!")
    if not filename:
        messagebox.showerror("Error", "No file name provided!")
        return None
    return f"{folderpath}/{filename}.csv"


def initialize_csv(CSV_FILE):
    try:
        with open(CSV_FILE, mode="x", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Frequency", "Amplitude", "Duration"])
    except FileExistsError:
        pass


def update_csv():
    freq = entry_freq.get()
    amp = entry_amp.get()
    dur = entry_dur.get()

    try:
        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([freq, amp, dur])
        print(
            f"Recorded! -> Frequency: {freq} (Hz), Amplitude: {amp} (nA), Duration: {dur} (sec)"
        )
    except Exception as e:
        messagebox.showerror("Error", f"Failed to write to CSV: {e}")

    # Clear input fields
    entry_freq.delete(0, tk.END)
    entry_amp.delete(0, tk.END)
    entry_dur.delete(0, tk.END)


def run_circuit():
    if not circuit:
        messagebox.showerror("Error", "Circuit not connected!")
        return

    try:
        dur = float(entry_dur.get())  # Convert duration to float
        circuit.trigger(1)
        time.sleep(dur)
        circuit.trigger(2)
        print("Circuit triggered successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run circuit: {e}")


def run_both():
    run_circuit()
    update_csv()


##### Initialization #####
circuit = connect_RM1()
CSV_FILE = name_csv()
if CSV_FILE:
    initialize_csv(CSV_FILE)

##### GUI #####
root = tk.Tk()
root.title("Stimulus Trigger App")

label_title = tk.Label(root, text="Stimulus Trigger App")
label_title.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

label_freq = tk.Label(root, text="Frequency (Hz)")
label_freq.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_freq = tk.Entry(root)
entry_freq.grid(row=1, column=1, padx=10, pady=5)

label_amp = tk.Label(root, text="Amplitude (nA)")
label_amp.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_amp = tk.Entry(root)
entry_amp.grid(row=2, column=1, padx=10, pady=5)

label_dur = tk.Label(root, text="Duration (s)")
label_dur.grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_dur = tk.Entry(root)
entry_dur.grid(row=3, column=1, padx=10, pady=5)

button_run = tk.Button(root, text="RUN!", command=run_both)
button_run.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
