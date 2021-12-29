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

# A tool that allows some operations on tile set images. Should support all common image formats.
# Requires Pillow (fork of PIL) to work.

import argparse
import os
import sys
import time
import math
from PIL import Image

parser = argparse.ArgumentParser('Performs common operations with tile set images.')
parser.add_argument(
    'input',
    help='Input file path',
    nargs=1
)
parser.add_argument(
    'mode',
    choices=['pad', 'extend', 'extract', 'compact', 'pow2', 'margin'],
    nargs=1
)
parser.add_argument(
    'params',
    nargs='*'
)
args = parser.parse_args()

input_file = args.input[0]
mode = args.mode[0]
params = args.params

directory, file = os.path.split(input_file)
name, ext = os.path.splitext(file)
output_path = directory + '/out' if mode == 'extract' else directory + '/' + name + '_out' + ext

image = Image.open(input_file)
out = None


def pad():
    global out
    new_spacing = int(params[PARAM_INDEX + 0])

    tw = (image.width + old_spacing) // (tile_width + old_spacing)
    th = (image.height + old_spacing) // (tile_height + old_spacing)

    nw = tile_width * tw + new_spacing * (tw - 1) + 2 * margin
    nh = tile_height * th + new_spacing * (th - 1) + 2 * margin
    out = Image.new('RGBA', (nw, nh))

    for ty in range(th):
        for tx in range(tw):
            x1 = tile_width * tx + old_spacing * tx + margin
            y1 = tile_height * ty + old_spacing * ty + margin
            x2 = x1 + tile_width
            y2 = y1 + tile_height
            tile = image.crop((x1, y1, x2, y2))

            x1 = tile_width * tx + new_spacing * tx + margin
            y1 = tile_height * ty + new_spacing * ty + margin
            out.paste(tile, (x1, y1))


def extend():
    global out
    new_spacing = int(params[PARAM_INDEX + 0])
    extension = int(params[PARAM_INDEX + 1])

    tw = (image.width + old_spacing) // (tile_width + old_spacing)
    th = (image.height + old_spacing) // (tile_height + old_spacing)

    nw = tile_width * tw + new_spacing * (tw - 1) + 2 * margin
    nh = tile_height * th + new_spacing * (th - 1) + 2 * margin
    out = Image.new('RGBA', (nw, nh))

    for ty in range(th):
        for tx in range(tw):
            x1 = tile_width * tx + old_spacing * tx + margin
            y1 = tile_height * ty + old_spacing * ty + margin
            x2 = x1 + tile_width
            y2 = y1 + tile_height
            tile = image.crop((x1, y1, x2, y2))

            x1 = tile_width * tx + new_spacing * tx + margin
            y1 = tile_height * ty + new_spacing * ty + margin
            out.paste(tile, (x1, y1))


def extract():
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    else:
        print('!!! Output file already exists !!!', file=sys.stderr)
        exit(-1)
    tw = (image.width + old_spacing) // (tile_width + old_spacing)
    th = (image.height + old_spacing) // (tile_height + old_spacing)

    i = 0
    for ty in range(th):
        for tx in range(tw):
            i += 1
            x1 = tile_width * tx + old_spacing * tx + margin
            y1 = tile_height * ty + old_spacing * ty + margin
            x2 = x1 + tile_width
            y2 = y1 + tile_height
            tile = image.crop((x1, y1, x2, y2))
            tile.save(output_path + '/' + str(i) + ext)


def compact():
    global out

    tw = (image.width + old_spacing) // (tile_width + old_spacing)
    th = (image.height + old_spacing) // (tile_height + old_spacing)

    nw = tile_width * tw + 2 * margin
    nh = tile_height * th + 2 * margin
    out = Image.new('RGBA', (nw, nh))

    for ty in range(th):
        for tx in range(tw):
            x1 = tile_width * tx + old_spacing * tx + margin
            y1 = tile_height * ty + old_spacing * ty + margin
            x2 = x1 + tile_width
            y2 = y1 + tile_height
            tile = image.crop((x1, y1, x2, y2))

            x1 = tile_width * tx + margin
            y1 = tile_height * ty + margin
            out.paste(tile, (x1, y1))


def pow2():
    global out
    nw = int(math.pow(2, math.ceil(math.log2(image.width))))
    nh = int(math.pow(2, math.ceil(math.log2(image.height))))
    out = Image.new('RGBA', (nw, nh))
    out.paste(image, (0, 0))


if len(params) >= 4:
    tile_width = int(params[0])
    tile_height = int(params[1])
    old_spacing = int(params[2])
    margin = int(params[3])
PARAM_INDEX = 4

start = time.time()
if mode == 'pad':
    pad()
elif mode == 'extend':
    extend()
elif mode == 'extract':
    extract()
elif mode == 'compact':
    compact()
elif mode == 'pow2':
    pow2()
elif mode == 'margin':
    new_margin = int(params[0])
    out = Image.new('RGBA', (image.width + 2 * new_margin, image.height + 2 * new_margin))
    out.paste(image, (new_margin, new_margin))

if out is not None:
    if os.path.exists(output_path):
        print('!!! Output file already exists !!!', file=sys.stderr)
        exit(-1)
    out.save(output_path)

end = time.time()
print(f'Done in {round(end - start, 3)}s.')
