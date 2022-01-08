import re
import tkinter as tk
import tkinter.font as tkf
from dataclasses import dataclass
from calculations import get_best_replacement, simplify_text, get_coords, \
    check_word_len, sentence_beginning
from files import read_file, file_to_dict, append_file
from menu import open_settings


def prepare_execution():
    global wrong_words
    global word_coords
    top_btn.value = ""
    bot_btn.value = ""
    word_coords = ()
    wrong_words = {}
    main_text.tag_remove("wrong", "1.0", tk.END)


def highlight_wrong_words():
    prepare_execution()
    text = main_text.get(1.0, tk.END).lower()
    simplified_text = simplify_text(text)
    for i in simplified_text:
        for j in re.split(r"[!#$%&'()\"*+,-./:;<=>?@[\]^_`{|}~]", i):
            first = get_best_replacement(j, words_dictionary, 
                                         main_data["method"])
            second = get_best_replacement(j, words_dictionary, 
                                          main_data["method"], first)
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
    word = main_text.get(f"@{event.x},{event.y} wordstart",
                         f"@{event.x},{event.y} wordend").lower()
    if word in wrong_words:
        is_beginning = sentence_beginning(
            main_text, main_text.index(f"@{event.x},{event.y} wordstart"))
        if is_beginning:
            top_btn.value = wrong_words[word]["replacements"][0].capitalize()
        else:
            top_btn.value = wrong_words[word]["replacements"][0]
        if is_beginning:
            bot_btn.value = wrong_words[word]["replacements"][1].capitalize()
        else:
            bot_btn.value = wrong_words[word]["replacements"][1]
        top_btn.element["text"] = check_word_len(top_btn.value)
        bot_btn.element["text"] = check_word_len(bot_btn.value)
        word_coords = (event.x, event.y)


def replace_word(button_value):
    if button_value != "":
        top_btn.value = ""
        bot_btn.value = ""
        top_btn.element["text"] = ""
        bot_btn.element["text"] = ""
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


@dataclass
class MyButton:
    value: str
    element: tk.Button


if __name__ == "__main__":
    main_data = file_to_dict()
    filename = main_data["dict_name"]
    words_dictionary = read_file(filename)
    if words_dictionary is None:
        raise ValueError("dictionary.txt file is empty.")

    root = tk.Tk()
    root.title("Spellchecker")

    main_font = tkf.Font(size=30)
    main_font_buttons = tkf.Font(size=30, weight='bold')

    main_text = tk.Text(root, font=main_font, foreground="#001219", 
                        width=40, height=6)
    top_btn = MyButton(
        "", tk.Button(font=main_font_buttons,
                      command=lambda: replace_word(top_btn.value)))
    bot_btn = MyButton(
        "", tk.Button(font=main_font_buttons, 
                      command=lambda: replace_word(bot_btn.value)))
    ready_btn = tk.Button(text="Ready", font=main_font_buttons, 
                          command=highlight_wrong_words)

    main_text.pack()
    top_btn.element.pack()
    bot_btn.element.pack()
    ready_btn.pack()

    main_text.tag_config("highlight", background="#94d2bd")
    main_text.tag_configure("wrong", foreground="#ae2012")

    main_text.bind("<Motion>", on_mouse_move)
    main_text.bind("<Button>", on_word_click)

    main_menu = tk.Menu(root)
    root.config(menu=main_menu)
    main_menu.add_command(label="Save words",
                          command=lambda: append_file(
                              filename, wrong_words.keys()))
    main_menu.add_command(label="Settings",
                          command=lambda: open_settings(root))

    root.mainloop()
