#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

desktop_dir = Path.home() / ".local/share/applications"

CATEGORIES = [
    "AudioVideo",
    "Audio",
    "Video",
    "Development",
    "Education",
    "Game",
    "Graphics",
    "Network",
    "Office",
    "Settings",
    "Utility",
]

def make_desktop_entry(name, exec_path, categories, icon=None, comment=None):
    entry = [
        "[Desktop Entry]",
        "Version=1.0",
        "Type=Application",
        f"Name={name}",
        f"Exec={exec_path}",
        f"Categories={';'.join(categories)};",
    ]
    if icon:
        entry.append(f"Icon={icon}")
    if comment:
        entry.append(f"Comment={comment}")

    file_path = desktop_dir / f"{name.lower().replace(' ', '-')}.desktop"
    with open(file_path, "w") as f:
        f.write("\n".join(entry) + "\n")

    return file_path

def refresh_applications():
    os.system("update-desktop-database ~/.local/share/applications")

def create_entry():
    name = name_var.get().strip()
    exec_path = exec_var.get().strip()
    icon = icon_var.get().strip() or None
    comment = comment_var.get().strip() or None

    # collect selected categories
    selected = [CATEGORIES[i] for i in cat_listbox.curselection()]
    if not selected:
        selected = ["Utility"]

    if not name or not exec_path:
        messagebox.showerror("Error", "Name and Executable are required.")
        return

    file_path = make_desktop_entry(name, exec_path, selected, icon, comment)
    refresh_applications()
    messagebox.showinfo("Success", f"Created {file_path}")

def browse_exec():
    path = filedialog.askopenfilename()
    if path:
        exec_var.set(path)

def browse_icon():
    path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.svg *.xpm")])
    if path:
        icon_var.set(path)

# GUI setup
root = tk.Tk()
root.title(".desktop Maker")

tk.Label(root, text="App Name").grid(row=0, column=0, sticky="w")
name_var = tk.StringVar()
tk.Entry(root, textvariable=name_var, width=40).grid(row=0, column=1)

tk.Label(root, text="Executable").grid(row=1, column=0, sticky="w")
exec_var = tk.StringVar()
tk.Entry(root, textvariable=exec_var, width=40).grid(row=1, column=1)
tk.Button(root, text="Browse", command=browse_exec).grid(row=1, column=2)

tk.Label(root, text="Categories").grid(row=2, column=0, sticky="nw")
cat_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=8, exportselection=False)
for cat in CATEGORIES:
    cat_listbox.insert(tk.END, cat)
cat_listbox.grid(row=2, column=1, sticky="w")

tk.Label(root, text="Icon").grid(row=3, column=0, sticky="w")
icon_var = tk.StringVar()
tk.Entry(root, textvariable=icon_var, width=40).grid(row=3, column=1)
tk.Button(root, text="Browse", command=browse_icon).grid(row=3, column=2)

tk.Label(root, text="Comment").grid(row=4, column=0, sticky="w")
comment_var = tk.StringVar()
tk.Entry(root, textvariable=comment_var, width=40).grid(row=4, column=1)

tk.Button(root, text="Create Entry", command=create_entry).grid(row=5, column=1, pady=10)

root.mainloop()

