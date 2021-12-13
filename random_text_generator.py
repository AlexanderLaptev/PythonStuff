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

import argparse
import random

latin_lower = 'qwertyuiopasdfghjklzxcvbnm'
latin_upper = latin_lower.upper()
cyrillic_lower = 'йцукенгшщзхъфывапролджэячсмитьбю'
cyrillic_upper = cyrillic_lower.upper()
numbers = '0123456789'
symbols = '!@#$%^&*()_+-=[]{};:\'"\\|,<.>/?№'
chars = latin_lower + latin_upper + cyrillic_upper + cyrillic_lower + numbers + symbols

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', action='store', nargs=1, required=True, help='The output file. Will be created.')
parser.add_argument('-l', '--length', action='store', nargs=1, required=True, help='The length of the produced file.')
args = parser.parse_args()
output_file_path = args.output[0]
length = int(args.length[0])

with open(output_file_path, 'x', encoding='utf_8') as file:
    for _ in range(length):
        file.write(random.choice(chars))
print('Done.')
