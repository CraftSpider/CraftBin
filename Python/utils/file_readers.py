"""
    A collection of file reading methods and tools. Because, well, it needs to be done a lot.

    Author: CraftSpider
"""

import json
import os


def overwrite_file(filename, data, mode="w"):
    """
        Overwrites the current data in a file with the provided string.
    :param filename: File to write over
    :param data: data to write to file.
    :param mode: mode to open file in
    """
    with open(filename, mode) as f:
        f.seek(0)
        f.write(data)


def load_file(filename):
    """
        Given a filename, returns it as an object in Read/Write form.
        Returns None if file doesn't exist.
    :param filename: File to open
    :return: file object.
    """
    try:
        f = open(filename, "r+")
        return f
    except FileNotFoundError:
        return None


def parse_file(filename, split_char=" "):
    """
        Takes a file, and splits each line into a list, using the 'split' variable
    :param filename: File to read from. Position is relative to running program by default. Type: String
    :param split_char: Sequence to split the line on. Type: String
    :return: List of file lines as lists.
    """
    out = []
    for line in open(filename):
        out += [line.strip().split(split_char)]
    if len(out) != 0 and out[-1][-1] == "\n":
        out[-1].pop()

    return out


def json_load(filename):
    """Loads a file as a JSON object and returns that"""
    with open(filename, 'a+') as file:
        try:
            file.seek(0)
            data = json.load(file)
        except json.JSONDecodeError:
            data = None
    return data


def json_save(filename, **kwargs):
    """Saves a file as valid JSON"""
    with open(filename, 'w+') as file:
        try:
            out = dict()
            for key in kwargs:
                out[key] = kwargs[key]
            json.dump(out, file, indent=2)
        except Exception as ex:
            print(ex)


def get_files_recursive(root, extension):
    rel_names = []
    for dir_name, dir_list, file_list in os.walk(root):
        for filename in file_list:
            if filename.endswith("." + extension):
                rel_names.append(dir_name + "/" + filename)
    return rel_names