# Copyright 2021 Alexander Laptev
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# A script to extract all unique characters from text files.
#
# * Specify files with the --files (-f) option,
# * Or provide a batch file with the --batch (-b) option.
# Each line of the batch file must contain a path to a file.

# A script used to take text from one or multiple files, get its unique symbols, and output them to another file.
# Created mainly for bitmap font generation for games.
#
# Arguments: [-h] [-f [FILES ...]] [-b [BATCH]] [-o OUTPUT]
# -h (--help) - prints help.
# -f (--files) - paths to files to be processed
# -b (--batch) - path to a file containing paths to the files to be processed on its every line.
# -o (--output) - path to the output file. Will be created if it doesn't exist. Will throw an exception if the file
#   already exists.
# All files must be UTF-8 encoded. Notepad++ does a great job converting text to UTF-8.
# I personally recommend using a batch file.
#
# === Average Performance ===
# All tests executed on plain text files encoded in UTF-8.
# * All 4 volumes of "War and Peace" (L. Tolstoy) in Russian [6.63 MiB]: 0.236s
# * Random text (latin & cyrillic alphanumeric + symbols) [81.1 MiB]: 1.9744s
# * Chinese lorem ipsum [4.4 KiB]: 0.003s

import argparse  # for parsing command line arguments.
import os  # for handling paths
import sys  # for printing errors.
import time  # for measuring the elapsed time.

charset = set()  # the set of all the unique characters of the files.


def process_path(path: str):
    global charset
    with open(path, 'r', encoding='utf_8') as file:
        contents = file.read()
        if not contents:  # skip file if it's empty.
            return
        contents = ''.join(contents.split())  # remove whitespace from the contents.
        charset = set.union(charset, set(contents))  # add the unique characters to the global charset.


def write_result_to_file(path: str):
    global charset
    with open(path, 'x', encoding='utf_8') as file:
        file.write(''.join(sorted(charset)))


# Get CMD arguments.
parser = argparse.ArgumentParser(description='Takes text from one or multiple files, gets its unique symbols, '
                                             'and outputs them to another file.'
                                 )
parser.add_argument('-f', '--files', action='store', nargs='*', help='Paths to files to be processed.')
parser.add_argument('-b', '--batch', action='store', nargs='?', help='Path to a file containing paths to the files to '
                                                                     'be processed on its every line.')
parser.add_argument('-o', '--output', action='store', nargs=1, required=True, help='Path to the output file.')
args = parser.parse_args()


def fail_with_message(message: str):
    parser.print_usage(file=sys.stderr)
    print(message, file=sys.stderr)
    exit(-1)


if args.files is None and args.batch is None:
    fail_with_message('Error: Neither the input files nor the batch file are specified.')
elif args.files is not None and args.batch is not None:
    fail_with_message('Error: Provided with both the input files and the batch file.')

if os.path.exists(args.output[0]):
    fail_with_message('Error: Output file already exists!')

paths_to_process = args.files
if args.files is None:
    with open(args.batch, 'r', encoding='utf_8') as file:
        paths_to_process = file.readlines()
if len(paths_to_process) == 0:
    fail_with_message('Error: No paths specified in the batch file.')

start_time = time.time()
for path in paths_to_process:
    path = path.strip()
    if not path:
        continue  # skip empty paths.
    with open(path, 'r', encoding='utf_8') as file:
        process_path(path)
try:
    write_result_to_file(args.output[0])
except FileExistsError:
    fail_with_message('Error: Output file already exists!')
end_time = time.time()
print(f'Done in {round(end_time - start_time, 3)}s.')
