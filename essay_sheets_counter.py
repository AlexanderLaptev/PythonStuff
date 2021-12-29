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

# A script used to calculate how many sheets of paper an essay takes.

AVERAGE_CHARACTERS_PER_LINE = 36  # The average number of characters per line (not including whitespace)
LINES_PER_PAGE = 23
PAGES_PER_SHEET = 2

symbols = int(input('Number of characters >> '))
lines = round(symbols / AVERAGE_CHARACTERS_PER_LINE, 2)
pages = round(lines / LINES_PER_PAGE, 2)
sheets = round(pages / PAGES_PER_SHEET, 2)

print(f'Lines: {lines}')
print(f'Pages: {pages}')
print(f'Sheets: {sheets}')
