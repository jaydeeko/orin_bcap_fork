import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import csv
import os
import shutil

# Paths for active files
DASHBOARD_TEMPLATE = "DashBoard.py"
PLANES_TEMPLATE = "planes.csv"
DASHBOARD_ACTIVE = "Dashboard_active.py"
PLANES_ACTIVE = "planes_active.csv"

# Create active files from templates if they don't exist
def create_active_files():
    if not os.path.exists(DASHBOARD_ACTIVE):
        shutil.copy(DASHBOARD_TEMPLATE, DASHBOARD_ACTIVE)
    if not os.path.exists(PLANES_ACTIVE):
        shutil.copy(PLANES_TEMPLATE, PLANES_ACTIVE)

# Function to load parameters from Dashboard_active.py
def load_parameters():
    try:
        global parameters
        parameters = {}
        with open(DASHBOARD_ACTIVE, "r") as file:
            for line in file:
                if "=" in line and not line.strip().startswith("#"):
                    key, value = map(str.strip, line.split("=", 1))
                    parameters[key] = value
        update_parameters_list()
    except FileNotFoundError:
        messagebox.showerror("Error", f"{DASHBOARD_ACTIVE} not found.")

# Function to update parameters listbox
def update_parameters_list():
    parameters_listbox.delete(0, tk.END)
    for key, value in parameters.items():
        parameters_listbox.insert(tk.END, f"{key} = {value}")

# Function to edit a parameter using a dialog box
def edit_parameter():
    try:
        selected = parameters_listbox.get(parameters_listbox.curselection())
        key = selected.split("=")[0].strip()
        current_value = parameters[key]

        # Open dialog box to edit value
        new_value = simpledialog.askstring(
            "Edit Parameter",
            f"Edit value for {key}:",
            initialvalue=current_value
        )

        # Revert to original value if left blank
        if new_value is not None:
            parameters[key] = new_value.strip() if new_value.strip() else current_value
        update_parameters_list()
    except Exception as e:
        messagebox.showerror("Error", f"Unable to edit parameter: {e}")

# Function to save updated parameters to Dashboard_active.py
def save_parameters():
    try:
        with open(DASHBOARD_ACTIVE, "w") as file:
            for key, value in parameters.items():
                file.write(f"{key} = {value}\n")
        messagebox.showinfo("Success", "Parameters saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Unable to save parameters: {e}")

# Function to process selected rows from the CSV file
def run_selected_rows():
    try:
        file_path = PLANES_ACTIVE
        if not os.path.exists(file_path):
            shutil.copy(PLANES_TEMPLATE, file_path)

        with open(file_path, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            rows = list(csv_reader)

        # Open the file for appending run results
        with open(file_path, "a") as csv_file:
            for i, (row, var) in enumerate(zip(rows, check_vars)):
                if var.get():
                    step = row.get("Step", "").strip()
                    if step in ["Pav", "Crown", "PavT", "CrownT"]:
                        FacetLoop(row, LapProcess, client, robot_handle)
                        print(f"Running FacetLoop for row {i+1}: {row}")
                    elif step == "Gird":
                        GirdleLoop(row, LapProcess, client, robot_handle)
                        print(f"Running GirdleLoop for row {i+1}: {row}")
                    else:
                        continue

                    # Log run completion with Dopheight
                    dopheight = parameters.get("Dopheight", "Unknown")
                    csv_file.write(f"{row}, Run, Dop = {dopheight}\n")

        messagebox.showinfo("Success", "Selected rows have been run.")
    except Exception as e:
        messagebox.showerror("Error", f"Unable to run selected rows: {e}")

# Function to load CSV rows into the GUI with checkboxes
def load_csv():
    try:
        file_path = PLANES_ACTIVE
        if not os.path.exists(file_path):
            shutil.copy(PLANES_TEMPLATE, file_path)

        with open(file_path, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            global check_vars
            check_vars = []
            for row in csv_reader:
                var = tk.BooleanVar()
                checkbutton = tk.Checkbutton(csv_frame, text=row, variable=var)
                checkbutton.pack(anchor="w")
                check_vars.append(var)

    except Exception as e:
        messagebox.showerror("Error", f"Unable to load CSV file: {e}")

# Create the main window
root = tk.Tk()
root.title("Dashboard & CSV Processor")

# Frame for parameters
param_frame = tk.LabelFrame(root, text="Dashboard Parameters")
param_frame.pack(fill="both", expand=True, padx=10, pady=10)

parameters_listbox = tk.Listbox(param_frame, height=10, width=50)
parameters_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)

param_scrollbar = tk.Scrollbar(param_frame, orient="vertical", command=parameters_listbox.yview)
parameters_listbox.config(yscrollcommand=param_scrollbar.set)
param_scrollbar.pack(side="right", fill="y")

edit_button = tk.Button(param_frame, text="Edit Parameter", command=edit_parameter)
edit_button.pack(padx=5, pady=5)

save_button = tk.Button(param_frame, text="Save Parameters", command=save_parameters)
save_button.pack(padx=5, pady=5)

# Frame for CSV processing
csv_frame = tk.LabelFrame(root, text="CSV Processing")
csv_frame.pack(fill="both", expand=True, padx=10, pady=10)

load_csv_button = tk.Button(csv_frame, text="Load CSV", command=load_csv)
load_csv_button.pack(padx=5, pady=5)

run_button = tk.Button(csv_frame, text="Run Selected Rows", command=run_selected_rows)
run_button.pack(padx=5, pady=5)

# Create active files and load parameters
create_active_files()
load_parameters()

# Run the main loop
root.mainloop()
