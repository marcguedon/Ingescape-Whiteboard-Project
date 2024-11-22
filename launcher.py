import subprocess
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


def select_exe():
    """Ouvre une boîte de dialogue pour sélectionner le chemin de l'exécutable."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Sélectionner votre raccourci bureau de votre application Ingescape Circle v4",
        filetypes=[("Executables", "*.exe")]
    )
    return file_path if file_path else None


def validate_inputs(port_entry, device_combobox, root, ingescape_circle_path, whiteboard_path, ingescape_project_path, processes):
    """Valide les entrées et lance les processus si elles sont correctes."""
    port = port_entry.get()
    device = device_combobox.get()

    if not port.isdigit():
        messagebox.showerror("Erreur", "Le port doit être un nombre valide.")
        port_entry.delete(0, tk.END)
        port_entry.insert(0, '1820')
        return

    messagebox.showinfo("Succès", f"Port: {port}\nDevice: {device}")
    root.quit()
    root.destroy()
    launch_processes(port, device, ingescape_circle_path, whiteboard_path, ingescape_project_path, processes)


def launch_processes(port, device, ingescape_circle_path, whiteboard_path, ingescape_project_path, processes):
    """Lance les processus nécessaires."""
    processes.extend([
        subprocess.Popen([whiteboard_path, '--port', port, '--device', device]),
        subprocess.Popen([ingescape_circle_path, ingescape_project_path, '--port', port, '--device', device]),
        subprocess.Popen(['python', 'Puissance4_View/src/main.py', '--port', port, '--device', device]),
        subprocess.Popen(['python', 'Puissance4_Controller/src/main.py', '--port', port, '--device', device])
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
    """Termine tous les processus."""
    for process in processes:
        process.terminate()
    print("Tous les processus ont été arrêtés.")


def create_parameter_window(ingescape_circle_path, whiteboard_path, ingescape_project_path, processes):
    """Crée la fenêtre pour paramétrer le port et le device."""
    root = tk.Tk()
    root.title("Paramétrage du port et du device")

    # Gestion de la fermeture pour arrêter les processus
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, processes))

    # Champ pour le port
    tk.Label(root, text="Entrez le port :").pack()
    port_entry = tk.Entry(root)
    port_entry.insert(0, '1820')
    port_entry.pack()

    # Liste déroulante pour le périphérique
    tk.Label(root, text="Choisissez le device :").pack()
    device_combobox = ttk.Combobox(root, values=["Wi-Fi", "Ethernet 5", "Loopback Pseudo-Interface 1"], state="readonly")
    device_combobox.set("Wi-Fi")
    device_combobox.pack()

    # Bouton pour valider
    tk.Button(
        root, text="Valider",
        command=lambda: validate_inputs(port_entry, device_combobox, root, ingescape_circle_path, whiteboard_path, ingescape_project_path, processes)
    ).pack()

    root.mainloop()


def on_close(root, processes):
    """Gestion de la fermeture de la fenêtre pour arrêter les processus."""
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
        terminate_processes(processes)
        root.quit()
        root.destroy()


def main():
    # Liste pour suivre les processus
    processes = []

    # Sélection de l'exécutable Ingescape Circle
    ingescape_circle_path = select_exe()
    if not ingescape_circle_path:
        print("Chemin de l'exécutable non sélectionné. Fermeture du programme.")
        return

    # Chemins relatifs à convertir en absolus
    relative_whiteboard_path = "Whiteboard.win64/Whiteboard/Whiteboard.exe"
    relative_ingescape_project_path = "puissance4.igssystem"

    whiteboard_path = os.path.abspath(relative_whiteboard_path)
    ingescape_project_path = os.path.abspath(relative_ingescape_project_path)

    # Créer la fenêtre de paramétrage
    create_parameter_window(ingescape_circle_path, whiteboard_path, ingescape_project_path, processes)


if __name__ == "__main__":
    main()
