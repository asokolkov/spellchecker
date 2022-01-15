import sys
import tkinter as tk
import tkinter.font as tkf
from menu import open_settings
from dataclasses import dataclass
from files import read_file, file_to_dict, append_file
from calculations import get_best_word, text_to_array, get_coords, \
    get_clicked_word


def highlight(words, text, correct_words):
    words.coords = ()
    words.wrong = []
    text.tag_remove("wrong", "1.0", tk.END)
    local_text = text.get(1.0, tk.END).lower()
    for i in text_to_array(local_text):
        if get_best_word(i, correct_words, main_data["method"]) != i:
            start, finish = get_coords(i, local_text)
            text.tag_add("wrong", start, finish)
            words.wrong.append(i)
        local_text = local_text.replace(i, "#" * len(i), 1)


def on_word_click(event, words, correct_words, text, top_btn, bot_btn):
    word, coords = get_clicked_word(event.x, event.y, text)
    word = word.lower()
    if word in words.wrong:
        first = get_best_word(word, correct_words, main_data["method"])
        second = get_best_word(word, correct_words, main_data["method"], first)
        top_btn["text"] = first
        bot_btn["text"] = second
        words.coords = coords


def replace_word(main_btn, other_btn, words, text):
    if main_btn["text"] != "":
        start = words.coords[0]
        finish = words.coords[1]
        text.delete(start, finish)
        text.insert(start, main_btn["text"])
        main_btn["text"] = ""
        other_btn["text"] = ""


def on_mouse_move(event, words, text):
    text.tag_remove("highlight", "1.0", tk.END)
    word, coords = get_clicked_word(event.x, event.y, text)
    if word.lower() in words.wrong:
        text.tag_add("highlight", coords[0], coords[1])


@dataclass
class Words:
    wrong: list
    coords: tuple


def main():
    filename = main_data["dict_name"]
    correct_words = read_file(filename)

    if not correct_words:
        print("dictionary.txt file is empty.")
        sys.exit(1)

    words = Words([], (0, 0))

    root = tk.Tk()
    root.title("Spellchecker")

    text = tk.Text(root, font=tkf.Font(size=30), foreground="#001219",
                   width=40, height=6)
    top_btn = tk.Button(
        font=tkf.Font(size=30),
        command=lambda: replace_word(top_btn, bot_btn, words, text))
    bot_btn = tk.Button(
        font=tkf.Font(size=30),
        command=lambda: replace_word(bot_btn, top_btn, words, text))
    ready_btn = tk.Button(
        text="Ready", font=tkf.Font(size=30, weight='bold'),
        command=lambda: highlight(words, text, correct_words))

    text.pack()
    top_btn.pack(fill="both")
    bot_btn.pack(fill="both")
    ready_btn.pack(fill="both")

    text.tag_config("highlight", background="#94d2bd")
    text.tag_configure("wrong", foreground="#ae2012")

    text.bind("<Motion>", lambda event: on_mouse_move(event, words, text))
    text.bind(
        "<Button>", lambda event: on_word_click(
            event, words, correct_words, text, top_btn, bot_btn))

    main_menu = tk.Menu(root)
    root.config(menu=main_menu)
    main_menu.add_command(label="Save words",
                          command=lambda: append_file(filename, words.wrong))
    main_menu.add_command(label="Settings",
                          command=lambda: open_settings(root))

    root.mainloop()


if __name__ == "__main__":
    main_data = file_to_dict()
    try:
        main()
    except Exception as e:
        print(e)
