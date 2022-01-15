import re
import Levenshtein


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


def get_best_word(word, sorted_dictionary, method, except_word=None):
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


def compress_coords(start, finish):
    a = start.split(".")
    b = finish.split(".")
    return f"{a[0]}.{int(a[1]) + 1}", f"{b[0]}.{int(b[1]) - 1}"


def get_clicked_word(x, y, text):
    pattern = re.compile("[a-zA-Zа-яА-Я0-9-]")
    result = ""
    clicked_coords = text.index(f"@{x},{y}"), text.index("current")
    text_coords = clicked_coords[0].split(".")
    row, col = int(text_coords[0]), int(text_coords[1])

    finish = f"{row}.{col + 1}"
    letter = text.get(f"{row}.{col}", finish)
    i = 1
    while pattern.match(letter):
        result += letter
        i += 1
        finish = f"{row}.{col + i}"
        letter = text.get(f"{row}.{col + i - 1}", finish)

    i = 1
    start = f"{row}.{col - 1}"
    letter = text.get(start, f"{row}.{col}")
    while pattern.match(letter):
        result = letter + result
        i += 1
        start = f"{row}.{col - i}"
        letter = text.get(start, f"{row}.{col - i + 1}")

    return result, compress_coords(start, finish)


def text_to_array(text):
    result = []
    for i in re.split("[^a-zA-Zа-яА-Я0-9-]", text):
        if not i.isdigit():
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
