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

# A script which adds a special padding between tiles in an existing tile set.
# Requires Pillow (PIL fork) to work.

import argparse

# region CLI arguments
parser = argparse.ArgumentParser(description='Extend tiles in a tile set for seamless rendering.')
parser.add_argument(
    '--input', '-i',
    help='Input path.',
    nargs=1,
    required=True
)
parser.add_argument(
    '--output', '-o',
    help='Output path. May be omitted.',
    nargs='?',
    required=False
)
parser.add_argument(
    '--mn',
    help='Margin.',
    nargs='+',
    default='0',
    required=False
)
parser.add_argument(
    '--ts',
    help='Tile spacing.',
    nargs='+',
    default='0',
    required=False
)
parser.add_argument(
    '--sz',
    help='Tile size.',
    nargs='+',
    required=True
)
parser.add_argument(
    '--nmn',
    help='New margin.',
    nargs='+',
    required=False
)
parser.add_argument(
    '--nts',
    help='New tile spacing.',
    nargs='+',
    required=False
)
parser.add_argument(
    '--el',
    help='Extension length.',
    nargs=1,
    default='1',
    required=False
)
args = parser.parse_args()
