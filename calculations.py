import re
import Levenshtein
import tkinter as tk


def distance(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n
    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add = previous_row[j] + 1
            delete = current_row[j - 1] + 1
            change = previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[n]


def get_best_replacement(word, sorted_dictionary, method, except_word=None):
    local_dictionary = sorted_dictionary.copy()
    if except_word is not None:
        local_dictionary.remove(except_word)
    min_distance = 1000000000000
    best_word = ""
    for i in local_dictionary:
        current_distance = Levenshtein.distance(word, i) \
            if method == "Imported" else distance(word, i)
        if current_distance < min_distance:
            min_distance = current_distance
            best_word = i
    return best_word


def simplify_text(text):
    result = []
    for i in text.split():
        if not i.isdigit() and (bool(re.search("[а-яА-Я]", i))
                                or bool(re.search("[a-zA-Z]", i))):
            result.append(i)
    return result


def get_coords(word, text):
    row = -1
    text_array = text.split("\n")
    for i in range(len(text_array)):
        if word in text_array[i]:
            row = i
            break
    start = text_array[row].index(word)
    finish = start + len(word)
    return f"{row + 1}.{start}", f"{row + 1}.{finish}"


def check_word_len(word):
    max_word_len = 16
    return word[:max_word_len] + "..." if len(word) > max_word_len else word


def sentence_beginning(main_text, start):
    start_row, start_column = start.split(".")
    text = main_text.get(1.0, tk.END).split("\n")
    row = text[int(start_row) - 1]
    index = int(start_column) - 2
    return True if index < 0 or \
                   row[index] == "." or \
                   row[index] == "!" or \
                   row[index] == "?" else False
