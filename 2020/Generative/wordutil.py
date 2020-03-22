import sys
import os


def arr2str(arr):
    line = ''
    for element in arr:
        line += element + ' '
    return line


def arr2lns(arr):
    lines = ''
    for ln in arr:
        for element in ln:
            lines += element
        lines += '\n'
    return lines


def swap(file_name, destroy):
    data = []
    for line in open(file_name, 'rb').readlines():
        data.append(line.replace('\n', ''))
    if destroy:
        os.remove(file_name)
    return data


def refresh_wordlist(file_name):
    words = list(swap(file_name, False))
    open(file_name, 'wb').write(arr2lns(list(set(words))))


if 'refresh' in sys.argv and len(sys.argv) > 2:
    refresh_wordlist(sys.argv[2])