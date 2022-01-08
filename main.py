import re
import tkinter as tk
import tkinter.font as tkf
from calculations import get_best_replacement, simplify_text, get_coords, \
    check_word_len, sentence_beginning, sort_dictionary
from files import read_file, file_to_dict, append_file
from menu import open_settings


def prepare_execution():
    global wrong_words
    global word_coords
    global first_btn_value
    global second_btn_value
    first_btn_value = ""
    second_btn_value = ""
    word_coords = ()
    wrong_words = {}
    main_text.tag_remove("wrong", "1.0", tk.END)


def highlight_wrong_words():
    prepare_execution()
    text = main_text.get(1.0, tk.END).lower()
    simplified_text = simplify_text(text)
    for i in simplified_text:
        for j in re.split(r"[!#$%&'()\"*+,-./:;<=>?@[\]^_`{|}~]", i):
            first = get_best_replacement(j, sorted_dictionary, method)
            second = get_best_replacement(j, sorted_dictionary, method, first)
            if first != j and second != j:
                start, finish = get_coords(j, text)
                main_text.tag_add("wrong", start, finish)
                wrong_words[f"{j}"] = {
                    "replacements": (first, second),
                    "indexes": (start, finish)
                }
            text = text.replace(j, "#" * len(j), 1)


def on_word_click(event):
    global word_coords
    global first_btn_value
    global second_btn_value
    word = main_text.get(f"@{event.x},{event.y} wordstart",
                         f"@{event.x},{event.y} wordend").lower()
    if word in wrong_words:
        is_beginning = sentence_beginning(
            main_text, main_text.index(f"@{event.x},{event.y} wordstart"))
        first_btn_value = wrong_words[word]["replacements"][0].capitalize() \
            if is_beginning else wrong_words[word]["replacements"][0]
        second_btn_value = wrong_words[word]["replacements"][1].capitalize() \
            if is_beginning else wrong_words[word]["replacements"][1]
        first_btn["text"] = check_word_len(first_btn_value)
        second_btn["text"] = check_word_len(second_btn_value)
        word_coords = (event.x, event.y)


def replace_word(button_value):
    global first_btn_value
    global second_btn_value
    if button_value != "":
        first_btn_value = ""
        second_btn_value = ""
        first_btn["text"] = ""
        second_btn["text"] = ""
        start = main_text.index(
            f"@{word_coords[0]},{word_coords[1]} wordstart")
        finish = main_text.index(
            f"@{word_coords[0]},{word_coords[1]} wordend")
        main_text.delete(start, finish)
        main_text.insert(start, button_value)


def on_mouse_move(event):
    main_text.tag_remove("highlight", "1.0", tk.END)
    word = main_text.get(f"@{event.x},{event.y} wordstart",
                         f"@{event.x},{event.y} wordend")
    if word.lower() in wrong_words:
        main_text.tag_add("highlight",
                          f"@{event.x},{event.y} wordstart",
                          f"@{event.x},{event.y} wordend")


wrong_words = {}
word_coords = (0, 0)
first_btn_value = ""
second_btn_value = ""


if __name__ == "__main__":
    main_data = file_to_dict()
    filename = main_data["dict_name"]
    sorted_dictionary = read_file(filename)
    if sorted_dictionary is None:
        raise ValueError("dictionary.txt file is empty.")
    sides = tk.N + tk.S + tk.W + tk.E
    method = main_data["method"]

    root = tk.Tk()
    root.resizable(width=False, height=False)
    root.title("Spellchecker")

    main_font = tkf.Font(size=30)
    main_font_buttons = tkf.Font(size=30, weight='bold')

    main_text = tk.Text(root, font=main_font, foreground="#001219",
                        background="#e9d8a6", width=40, height=8)
    ready_btn = tk.Button(text="Ready", font=main_font_buttons,
                          background="#e9d8a6", activebackground="#94d2bd",
                          command=highlight_wrong_words)
    first_btn = tk.Button(font=main_font_buttons, background="#e9d8a6",
                          activebackground="#94d2bd",
                          command=lambda: replace_word(first_btn_value))
    second_btn = tk.Button(font=main_font_buttons, background="#e9d8a6",
                           activebackground="#94d2bd",
                           command=lambda: replace_word(second_btn_value))
    main_text.grid(row=0, rowspan=6, column=0, columnspan=8, sticky=sides)
    ready_btn.grid(row=7, columnspan=8, sticky=sides)
    first_btn.grid(row=6, column=0, columnspan=4, sticky=sides)
    second_btn.grid(row=6, column=4, columnspan=4, sticky=sides)

    main_text.tag_config("highlight", background="#94d2bd")
    main_text.tag_configure("wrong", foreground="#ae2012")

    main_text.bind("<Motion>", on_mouse_move)
    main_text.bind("<Button>", on_word_click)

    main_menu = tk.Menu(root)
    root.config(menu=main_menu)
    main_menu.add_command(label="Save words",
                          command=lambda: append_file(
                              filename, wrong_words.keys()))
    main_menu.add_command(label="Sort dictionary",
                          command=lambda: sort_dictionary(filename))
    main_menu.add_command(label="Settings",
                          command=lambda: open_settings(root))

    root.mainloop()
