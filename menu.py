import tkinter as tk
from tkinter import ttk
import tkinter.font as tkf
from files import file_to_dict, dict_to_file


length = 5
sides = tk.N + tk.S + tk.W + tk.E


def clear_field(event):
    event.widget.delete(0, tk.END)


def save_data_and_close(settings, *fields):
    d = {}
    for i in fields:
        d[i[0]] = i[1].get()
    dict_to_file(d)
    settings.destroy()


def open_settings(root):
    settings = tk.Toplevel(root)
    settings.title("Spellchecker Settings")
    settings.resizable(width=False, height=False)

    font = tkf.Font(size=30)

    settings_l = tk.Label(settings, text="Settings",
                          font=tkf.Font(size=30, weight='bold'), anchor=tk.W)
    dict_path_l = tk.Label(settings, text="Dictionary Name", font=font,
                           anchor=tk.W)
    dict_name_e = tk.Entry(settings, font=font)
    dist_method_l = tk.Label(settings, text="Levenshtein Distance Method",
                             font=font, anchor=tk.W)
    dist_method_box = ttk.Combobox(settings, values=["Imported", "Handmade"])

    placeholders(dict_name_e, dist_method_box)

    dict_name_e.bind("<FocusIn>", clear_field)

    settings_l.grid(row=0, sticky=sides, pady=length, padx=length)
    dict_path_l.grid(row=1, column=0, sticky=sides, pady=length, padx=length)
    dict_name_e.grid(row=1, column=1, sticky=sides, pady=length, padx=length)
    dist_method_l.grid(row=2, column=0, sticky=sides, pady=length, padx=length)
    dist_method_box.grid(row=2, column=1, sticky=sides, pady=length,
                         padx=length)

    settings.protocol(
        "WM_DELETE_WINDOW",
        lambda s=settings, a=("dict_name", dict_name_e), b=("method",
                                                            dist_method_box):
        save_data_and_close(s, a, b))


def placeholders(dict_name_e, dist_method_box):
    data = file_to_dict()
    dict_name_e.delete(0, tk.END)
    if "dict_name" not in data or data["dict_name"] == '':
        dict_name_e.insert(0, "dictionary.txt")
    else:
        dict_name_e.insert(0, data["dict_name"])
    dist_method_box.current(
        dist_method_box["values"].index(data["method"])
        if "method" in data else 0)
