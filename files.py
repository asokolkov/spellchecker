import json


def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            array = file.readlines()
            if len(array) == 0:
                raise ValueError("dictionary.txt file is empty.")
            result = []
            for i in array:
                result.append(i.replace("\n", ""))
            return result
    except (FileExistsError, FileNotFoundError):
        open("dictionary.txt", "w+").close()
        d = file_to_dict()
        d["dict_name"] = "dictionary.txt"
        dict_to_file(d)


def append_file(filename, array):
    with open(filename, "a", encoding="utf-8") as f:
        for i in array:
            f.write(i + "\n")


def file_to_dict():
    d = {}
    try:
        with open("run_data_do_not_change_or_rename.txt", "r") as f:
            d = json.loads(f.read().replace("'", "\""))
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        open("run_data_do_not_change_or_rename.txt", "w+").close()
    return d


def dict_to_file(dictionary):
    with open("run_data_do_not_change_or_rename.txt", "w") as f:
        f.write(json.dumps(dictionary))
