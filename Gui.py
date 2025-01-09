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
        # Copy template and add 'Status' column with 'Pending' for all rows
        with open(PLANES_TEMPLATE, "r") as template_file:
            csv_reader = csv.DictReader(template_file)
            rows = list(csv_reader)

            # Ensure 'Status' column exists
            if rows and 'Status' not in rows[0]:
                for row in rows:
                    row['Status'] = "Pending"

            # Write to active file
            with open(PLANES_ACTIVE, "w", newline="") as active_file:
                fieldnames = csv_reader.fieldnames + ['Status'] if 'Status' not in csv_reader.fieldnames else csv_reader.fieldnames
                writer = csv.DictWriter(active_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

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
            create_active_files()

        with open(file_path, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            rows = list(csv_reader)
            completed_rows = []

        # Open the file for updating run results
        with open(file_path, "w", newline="") as csv_file:
            fieldnames = rows[0].keys() if rows else []
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

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

                    # Update row status and move to completed
                    row["Status"] = f"Cut, {parameters.get('Dopheight', 'Unknown')}"
                    completed_rows.append(row)
                else:
                    writer.writerow(row)

            # Append completed rows at the bottom
            for completed_row in completed_rows:
                writer.writerow(completed_row)

        messagebox.showinfo("Success", "Selected rows have been run and moved to the bottom.")
        load_csv()  # Reload the CSV to reflect updates in the GUI
    except Exception as e:
        messagebox.showerror("Error", f"Unable to run selected rows: {e}")

# Function to load CSV rows into the GUI with checkboxes
def load_csv():
    try:
        file_path = PLANES_ACTIVE
        if not os.path.exists(file_path):
            create_active_files()

        with open(file_path, "r", newline="") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            global check_vars
            check_vars = []

            # Clear previous rows
            for widget in csv_rows_frame.winfo_children():
                widget.destroy()

            # Add headers
            headers = csv_reader.fieldnames
            if headers is None:
                raise ValueError("The CSV file has no headers. Please check the file format.")

            headers_display = tk.Label(csv_rows_frame, text=" | ".join(headers), anchor="w", justify="left", font=("Helvetica", 10, "bold"))
            headers_display.grid(row=0, column=0, sticky="w")

            # Add rows with checkboxes
            for row_index, row in enumerate(csv_reader, start=1):
                var = tk.BooleanVar()
                row_display = " | ".join(row.get(header, "") for header in headers)
                checkbutton = tk.Checkbutton(csv_rows_frame, text=row_display, variable=var, anchor="w", justify="left")
                checkbutton.grid(row=row_index, column=0, sticky="w")
                check_vars.append(var)

            # Update canvas scroll region
            csv_canvas.update_idletasks()
            csv_canvas.configure(scrollregion=csv_canvas.bbox("all"))

    except FileNotFoundError:
        messagebox.showerror("Error", f"The file {PLANES_ACTIVE} was not found.")
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
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

csv_canvas = tk.Canvas(csv_frame)
csv_canvas.pack(side="left", fill="both", expand=True)

csv_scrollbar = tk.Scrollbar(csv_frame, orient="vertical", command=csv_canvas.yview)
csv_scrollbar.pack(side="right", fill="y")

csv_canvas.configure(yscrollcommand=csv_scrollbar.set)

csv_rows_frame = tk.Frame(csv_canvas)
csv_canvas.create_window((0, 0), window=csv_rows_frame, anchor="nw")

csv_rows_frame.bind("<Configure>", lambda e: csv_canvas.configure(scrollregion=csv_canvas.bbox("all")))

load_csv_button = tk.Button(root, text="Load CSV", command=load_csv)
load_csv_button.pack(padx=5, pady=5)

run_button = tk.Button(root, text="Run Selected Rows", command=run_selected_rows)
run_button.pack(padx=5, pady=5)

# Create active files and load parameters
create_active_files()
load_parameters()

# Run the main loop
root.mainloop()