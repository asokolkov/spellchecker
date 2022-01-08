import tkinter as tk
import tkinter.font as tkf
from dataclasses import dataclass
from calculations import get_best_word, simplify_text, get_coords, sentence_beginning
from files import read_file, file_to_dict, append_file
from menu import open_settings


def highlight_wrong_words():
    words.coords = ()
    words.wrong = []
    text.tag_remove("wrong", "1.0", tk.END)
    local_text = text.get(1.0, tk.END).lower()
    for i in simplify_text(local_text):
        if get_best_word(i, dictionary, main_data["method"]) != i:
            start, finish = get_coords(i, local_text)
            text.tag_add("wrong", start, finish)
            words.wrong.append(i)
        local_text = local_text.replace(i, "#" * len(i), 1)


def on_word_click(event):
    word = text.get(f"@{event.x},{event.y} wordstart",
                         f"@{event.x},{event.y} wordend").lower()
    if word in words.wrong:
        is_beginning = sentence_beginning(
            text, text.index(f"@{event.x},{event.y} wordstart"))
        first = get_best_word(word, dictionary, main_data["method"])
        second = get_best_word(word, dictionary, main_data["method"], first)
        top_btn["text"] = first.capitalize() if is_beginning else first
        bot_btn["text"] = second.capitalize() if is_beginning else second
        words.coords = (event.x, event.y)


def replace_word(button):
    if button["text"] != "":
        start = text.index(
            f"@{words.coords[0]},{words.coords[1]} wordstart")
        finish = text.index(
            f"@{words.coords[0]},{words.coords[1]} wordend")
        text.delete(start, finish)
        text.insert(start, button["text"])
        top_btn["text"] = ""
        bot_btn["text"] = ""


def on_mouse_move(event):
    text.tag_remove("highlight", "1.0", tk.END)
    word = text.get(f"@{event.x},{event.y} wordstart",
                         f"@{event.x},{event.y} wordend")
    if word.lower() in words.wrong:
        text.tag_add("highlight",
                          f"@{event.x},{event.y} wordstart",
                          f"@{event.x},{event.y} wordend")


@dataclass
class Words:
    wrong: list
    coords: tuple


if __name__ == "__main__":
    main_data = file_to_dict()
    filename = main_data["dict_name"]
    dictionary = read_file(filename)
    if dictionary is None:
        raise ValueError("dictionary.txt file is empty.")

    words = Words([], (0, 0))

    root = tk.Tk()
    root.title("Spellchecker")

    main_font = tkf.Font(size=30)
    btn_font = tkf.Font(size=30, weight='bold')

    text = tk.Text(root, font=main_font, foreground="#001219", 
                        width=40, height=6)
    top_btn = tk.Button(font=btn_font, command=lambda: replace_word(top_btn))
    bot_btn = tk.Button(font=btn_font, command=lambda: replace_word(bot_btn))
    ready_btn = tk.Button(text="Ready", font=btn_font, 
                          command=highlight_wrong_words)

    text.pack()
    top_btn.pack()
    bot_btn.pack()
    ready_btn.pack()

    text.tag_config("highlight", background="#94d2bd")
    text.tag_configure("wrong", foreground="#ae2012")

    text.bind("<Motion>", on_mouse_move)
    text.bind("<Button>", on_word_click)

    main_menu = tk.Menu(root)
    root.config(menu=main_menu)
    main_menu.add_command(label="Save words",
                          command=lambda: append_file(
                              filename, words.wrong))
    main_menu.add_command(label="Settings",
                          command=lambda: open_settings(root))

    root.mainloop()
