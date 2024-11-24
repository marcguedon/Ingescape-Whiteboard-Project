import subprocess
import os
import tkinter as tk
from tkinter import ttk, filedialog

def select_exe():
    """
    Open a dialog box to select the path of the executable
    """

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select the Ingescape Circle v4 executable",
        filetypes=[("Executables", "*.exe")]
    )
    
    return file_path if file_path else None


def validate_inputs(port_entry, device_combobox, root, ingescape_circle_path, whiteboard_path, ingescape_project_path, processes):
    """
    Validate the inputs and launch the processes if they are correct
    Inputs:
        port_entry: field for the port
        device_combobox: drop-down list for the device
        root: settings window
        ingescape_circle_path: path to the Ingescape Circle (v4) executable
        whiteboard_path: path to the Whiteboard executable
        ingescape_project_path: path to the Ingescape project
        processes: list to keep track of the processes
    """

    port = port_entry.get()
    device = device_combobox.get()

    root.quit()
    root.destroy()

    launch_processes(port, device, ingescape_circle_path, whiteboard_path, ingescape_project_path, processes)


def launch_processes(port, device, ingescape_circle_path, whiteboard_path, ingescape_project_path, processes):
    """
    Run the necessary processes
    Inputs:
        port: port for communication
        device: device for communication
        ingescape_circle_path: path to the Ingescape Circle (v4) executable
        whiteboard_path: path to the Whiteboard executable
        ingescape_project_path: path to the Ingescape project
        processes: list to keep track of the processes
    """

    processes.extend([
        subprocess.Popen([whiteboard_path, '--port', port, '--device', device]),
        subprocess.Popen([ingescape_circle_path, ingescape_project_path, '--port', port, '--device', device]),
        subprocess.Popen(['python', os.path.abspath('Puissance4_View/src/main.py'), '--port', port, '--device', device]),
        subprocess.Popen(['python', os.path.abspath('Puissance4_Controller/src/main.py'), '--port', port, '--device', device])
    ])

    try:
        while True:
            for process in processes:
                if process.poll() is not None:
                    terminate_processes(processes)
                    return
                
    except KeyboardInterrupt:
        terminate_processes(processes)


def terminate_processes(processes):
    """
    Stop all the processes
    Input:
        processes: list of processes to terminate
    """

    for process in processes:
        process.terminate()

    print("All processes have been stopped.")

def validate_port(action, value):
    """
    Validate the port
    Inputs:
        action: action performed
        value: value entered
    """

    if action == "1": # 1 -> insert a character
        return value.isdigit() and len(value) <= 4
    
    return True

def create_parameter_window(ingescape_circle_path, whiteboard_path, ingescape_project_path, processes):
    """
    Create the window to set the port and device
    Inputs:
        ingescape_circle_path: path to the Ingescape Circle (v4) executable
        whiteboard_path: path to the Whiteboard executable
        ingescape_project_path: path to the Ingescape project
        processes: list of processes
    """

    root = tk.Tk()
    root.title("Set the port and device")
    root.geometry("300x120")

    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, processes))

    tk.Label(root, text="Enter port:").pack()
    vcmd = root.register(validate_port)
    port_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%d', '%P'))
    port_entry.insert(0, '5670')
    port_entry.pack()

    tk.Label(root, text="Choose the device:").pack()
    device_combobox = ttk.Combobox(root, values=["Wi-Fi", "Ethernet 5", "Loopback Pseudo-Interface 1"], state="readonly")
    device_combobox.set("Wi-Fi")
    device_combobox.pack()

    tk.Button(
        root, text="Validate",
        command=lambda: validate_inputs(port_entry, device_combobox, root, ingescape_circle_path, whiteboard_path, ingescape_project_path, processes)
    ).pack()

    root.mainloop()


def on_close(root, processes):
    """
    Management of the window closing to stop the processes
    Inputs:
        root: main window
        processes: list of processes to terminate
    """

    terminate_processes(processes)
    root.quit()
    root.destroy()

def main():
    processes = []

    ingescape_circle_path = select_exe()

    if not ingescape_circle_path:
        print("Path to the executable not selected. Closing the program.")
        return

    whiteboard_path = os.path.abspath("Whiteboard.win64/Whiteboard/Whiteboard.exe")
    ingescape_project_path = os.path.abspath("puissance4.igssystem")

    create_parameter_window(ingescape_circle_path, whiteboard_path, ingescape_project_path, processes)

if __name__ == "__main__":
    main()
