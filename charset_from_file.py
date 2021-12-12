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

import argparse
import time
import os

charset = set()


def process_path(input_file_path: str):
    with open(input_file_path, encoding='utf_8') as input_file:
        global charset
        content = input_file.read()
        content = ''.join(content.split())
        charset = set.union(charset, set(content))


def write_charset_to_file(output_file_path):
    with open(output_file_path, encoding='utf_8', mode='w') as output_file:
        output_file.write(''.join(sorted(charset)))


parser = argparse.ArgumentParser(description='Get charset from text files.')
parser.add_argument('-f', '--files', action='store', nargs='*', help='The files to be processed.')
parser.add_argument('-b', '--batch', action='store', nargs='?', help='The file containing paths to the files to be '
                                                                     'processed.')
parser.add_argument('-o', '--output', action='store', help='The output file.')
args = parser.parse_args()
files = args.files

if args.output is None:
    raise RuntimeError('Output file is not specified.')
if args.batch is not None and files is not None:
    raise RuntimeError('Both batch and files are specified.')

if args.batch is not None:
    with open(args.batch, encoding='utf_8') as batch_file:
        paths = batch_file.readlines()
        start_time = time.time()
        for path in paths:
            path = path.strip()
            process_path(os.path.join(path))
        end_time = time.time()
        print(f'Done in {round(end_time - start_time, 3)} seconds.')
        write_charset_to_file(args.output)
else:
    start_time = time.time()
    for file in files:
        process_path(file)
    end_time = time.time()
    print(f'Done in {round(end_time - start_time, 3)} seconds.')
    write_charset_to_file(args.output)
