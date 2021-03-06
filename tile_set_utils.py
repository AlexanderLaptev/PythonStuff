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

# General usage: [-w] <input path> <mode> [params]
# Available modes: layout, pow2, extract, extrude.
#
# Output file/directory is either <current dir>/<input file>_out.<extension> or <current dir>/out, depending on
# the mode.
#
# Options:
# -w: Overwrite existing files. Does not overwrite directories (e.g. for the 'extract' mode).
#
# Mode descriptions
# layout: change padding and/or margin.
# pow2: make each dimension of the image a power of two (e.g. 184x652 -> 256x1024).
# extract: extract tiles from the image.
# extrude: tries to fix tile rendering artifacts by extruding the sides of each tile.
#
# Params for modes:
# layout: <tile width> <tile height> <old spacing> <old margin> <new spacing> <new margin>
# pow2: no parameters
# extract: <tile width> <tile height> <spacing> <margin>
# extrude: <tile width> <tile height> <spacing> <margin> <extrusion length>
#
# Example:
#
# Remove spacing and margin:
# -w test/test.png layout 64 64 2 1 0 0
# Overwrite output file test/test.png (relative to the script directory). Set mode to 'layout'.
# Tile width = 64, tile height = 64
# Old spacing = 2, old margin = 1
# New spacing = 0, new margin = 0
#
# Extrude sides:
# -w test/test.png extrude 64 64 0 0 1
# Overwrite output file, set mode to 'extrude'.
# Tile width = 64, tile height = 64
# No spacing, no margin
# Extrude 1 px
#
# Notes:
# When importing an extruded tile set, set spacing and margin as follows:
# spacing = 2 * <extrusion length> + <original spacing> (e.g. 2 * 1 + 2 = 4)
# margin = <original margin> + <extrusion length>
#
# The script has undergone some testing, but it may be unstable. Please report any issues on the GitHub issue tracker.

import argparse
import math
import os
import sys
import time

from PIL import Image

MODES = {
    'layout': None,
    'pow2': None,
    'extract': None,
    'extrude': None,
}
PARAMS_ERROR = 'Invalid number of parameters'


# region General purpose functions
def halt(msg: str):
    print('!!! Error: ' + msg + ' !!!', file=sys.stderr)
    sys.exit(-1)
# endregion


# region Parse required arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    '-w', '--overwrite',
    help='Overwrite output if it exists.',
    action='store_true'
)
parser.add_argument(
    'input',
    help='Input file path.',
    nargs=1
)
parser.add_argument(
    'mode',
    choices=MODES,
    nargs=1
)
parser.add_argument(
    'params',
    nargs='*'
)
args = parser.parse_args()

input_path = args.input[0]
overwrite = args.overwrite
mode = args.mode[0]
params = args.params
# endregion

# region Determine output path
directory, file = os.path.split(input_path)
name, extension = os.path.splitext(file)
output_path = directory + '/out' if mode == 'extract' else directory + '/' + name + '_out' + extension

# Check if the output path already exists
if os.path.exists(output_path):
    if not overwrite or mode == 'extract':
        halt('Output dir/file already exists')
    else:
        print('> Output path exists, overwriting.')
        os.remove(output_path)
else:
    if mode == 'extract':
        os.makedirs(output_path)
# endregion

# region Processing functions
def layout():
    if len(params) != 6:
        halt(PARAMS_ERROR)
    tile_width = int(params[0])
    tile_height = int(params[1])
    old_spacing = int(params[2])
    old_margin = int(params[3])
    new_spacing = int(params[4])
    new_margin = int(params[5])
    image = Image.open(input_path)

    # Derived using "complicated" algebra.
    tiles_horizontal = (image.width - 2 * old_margin + old_spacing) // (tile_width + old_spacing)
    tiles_vertical = (image.height - 2 * old_margin + old_spacing) // (tile_height + old_spacing)

    new_width = 2 * new_margin + tile_width * tiles_horizontal + new_spacing * (tiles_horizontal - 1)
    new_height = 2 * new_margin + tile_height * tiles_vertical + new_spacing * (tiles_vertical - 1)
    output = Image.new('RGBA', (new_width, new_height))

    for tile_y in range(tiles_vertical):
        for tile_x in range(tiles_horizontal):
            # Extract tile
            x1 = old_margin + (tile_width + old_spacing) * tile_x
            y1 = old_margin + (tile_height + old_spacing) * tile_y
            x2 = x1 + tile_width
            y2 = y1 + tile_height
            tile = image.crop((x1, y1, x2, y2))

            x1 = new_margin + (tile_width + new_spacing) * tile_x
            y1 = new_margin + (tile_height + new_spacing) * tile_y
            output.paste(tile, (x1, y1))
    output.save(output_path, optimize=True)


def pow2():
    image = Image.open(input_path)
    new_width = 2 ** math.ceil(math.log2(image.width))
    new_height = 2 ** math.ceil(math.log2(image.height))
    out = Image.new('RGBA', (new_width, new_height))
    out.paste(image, (0, 0))
    out.save(output_path, optimize=True)


def extract():
    if len(params) != 4:
        halt(PARAMS_ERROR)
    tile_width = int(params[0])
    tile_height = int(params[1])
    old_spacing = int(params[2])
    old_margin = int(params[3])
    image = Image.open(input_path)

    tiles_horizontal = (image.width - 2 * old_margin + old_spacing) // (tile_width + old_spacing)
    tiles_vertical = (image.height - 2 * old_margin + old_spacing) // (tile_height + old_spacing)

    index = 0
    for tile_y in range(tiles_vertical):
        for tile_x in range(tiles_horizontal):
            index += 1

            # Extract tile
            x1 = old_margin + (tile_width + old_spacing) * tile_x
            y1 = old_margin + (tile_height + old_spacing) * tile_y
            x2 = x1 + tile_width
            y2 = y1 + tile_height
            tile = image.crop((x1, y1, x2, y2))

            tile.save(output_path + '/' + str(index) + extension, optimize=True)


def extrude():
    if len(params) != 5:
        halt(PARAMS_ERROR)
    tile_width = int(params[0])
    tile_height = int(params[1])
    spacing = int(params[2])
    margin = int(params[3])
    extrusion_length = int(params[4])
    image = Image.open(input_path)

    tiles_horizontal = (image.width - 2 * margin + spacing) // (tile_width + spacing)
    tiles_vertical = (image.height - 2 * margin + spacing) // (tile_height + spacing)

    new_width = 2 * margin + \
                tile_width * tiles_horizontal + \
                spacing * (tiles_horizontal - 1) + \
                2 * extrusion_length * tiles_horizontal
    new_height = 2 * margin + \
                 tile_height * tiles_vertical + \
                 spacing * (tiles_vertical - 1) + \
                 2 * extrusion_length * tiles_vertical
    out = Image.new('RGBA', (new_width, new_height))

    for tile_y in range(tiles_vertical):
        for tile_x in range(tiles_horizontal):
            # Extract tile
            x1 = margin + (tile_width + spacing) * tile_x
            y1 = margin + (tile_height + spacing) * tile_y
            x2 = x1 + tile_width
            y2 = y1 + tile_height
            tile = image.crop((x1, y1, x2, y2))

            # Paste
            x1 = margin + extrusion_length + (2 * extrusion_length + tile_width + spacing) * tile_x
            y1 = margin + extrusion_length + (2 * extrusion_length + tile_height + spacing) * tile_y
            out.paste(tile, (x1, y1))

            # region Extrude
            # I really hate this part because of the repetitive code, but there seems to be no way around this.
            # Left
            strip = tile.crop((0, 0, 1, tile_height))  # I spent half a day figuring all the coordinates in this script.
            for i in range(extrusion_length):
                out.paste(strip, (x1 - 1 - i, y1))

            # Right
            strip = tile.crop((tile_width - 1, 0, tile_width, tile_height))
            for i in range(extrusion_length):
                out.paste(strip, (x1 + tile_width + i, y1))

            # Top
            strip = tile.crop((0, 0, tile_width, 1))
            for i in range(extrusion_length):
                out.paste(strip, (x1, y1 - 1 - i))

            # Bottom
            strip = tile.crop((0, tile_height - 1, tile_width, tile_height))
            for i in range(extrusion_length):
                out.paste(strip, (x1, y1 + tile_height + i))
            # endregion

    out.save(output_path, optimize=True)
    print(f'> New spacing: {2 * extrusion_length + spacing} px.')
    print(f'> New margin: {margin + extrusion_length} px.')


MODES['layout'] = layout
MODES['pow2'] = pow2
MODES['extract'] = extract
MODES['extrude'] = extrude
# endregion

func = MODES[mode]
if func is None:
    halt('Mode not yet implemented')
else:
    start = time.time()  # perf_counter() is too precise for such tasks.
    func()
    end = time.time()
    print(f'Done in {round(end - start, 3)}s.')
