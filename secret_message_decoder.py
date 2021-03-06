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

# A CLI decoder for secret messages. Created mainly for decoding those from Andy's Apple Farm, but may be used for any
# ASCII (e.g. English) ciphers, I guess.
#
# Supports: Atbash cipher, Caesar cipher, Binary, Hexadecimal, Morse code.

import binascii
from enum import Enum, auto

SEPARATOR = '=' * 24

NEW_MESSAGE_COMMAND = 'new'
MORSE = {  # Copied from StackOverflow and pretty-printed with another small Python script.
    '-': 'T',
    '--': 'M',
    '---': 'O',
    '-----': '0',
    '----.': '9',
    '---..': '8',
    '--.': 'G',
    '--.-': 'Q',
    '--..': 'Z',
    '--...': '7',
    '-.': 'N',
    '-.-': 'K',
    '-.--': 'Y',
    '-.-.': 'C',
    '-..': 'D',
    '-..-': 'X',
    '-...': 'B',
    '-....': '6',
    '.': 'E',
    '.-': 'A',
    '.--': 'W',
    '.---': 'J',
    '.----': '1',
    '.--.': 'P',
    '.-.': 'R',
    '.-..': 'L',
    '..': 'I',
    '..-': 'U',
    '..---': '2',
    '..-.': 'F',
    '...': 'S',
    '...-': 'V',
    '...--': '3',
    '....': 'H',
    '....-': '4',
    '.....': '5'
}
EXIT_COMMANDS = ('exit', 'quit', 'e', 'q')
EXIT_COMMANDS_JOINED = ' | '.join(EXIT_COMMANDS)

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
ALPHABET_LENGTH = len(ALPHABET)
SAMPLE_MAX_LENGTH = 14


class Mode(Enum):
    ATBASH = auto()
    CAESAR = auto()
    BINARY = auto()
    HEXADECIMAL = auto()
    MORSE = auto()


# Splits `iterable` in chunks of `size` elements. Used by the binary and hexadecimal decoders.
def chunks(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]


def decrypt_atbash(string: str):
    result = []
    for char in string:
        is_upper_case = char.isupper()
        c = char.casefold()
        index = ALPHABET.find(c)
        if index == -1:
            result += char
        else:
            c = ALPHABET[-index - 1]
            if is_upper_case:
                c = c.upper()
            result += c
    return ''.join(result)  # 3 milliseconds saved on concatenating strings is 3 milliseconds!


def shift_letters(string: str, shift: int):  # Shift may be both positive and negative.
    result = []
    for char in string:
        is_upper_case = char.isupper()
        c = char.casefold()
        index = ALPHABET.find(c)
        if index == -1:
            result += char
        else:
            new_index = (index + shift) % ALPHABET_LENGTH
            c = ALPHABET[new_index]
            if is_upper_case:
                c = c.upper()
            result += c
    return ''.join(result)


def sample_caesar(string: str):
    str_length = len(string)
    should_print_ellipsis = str_length > SAMPLE_MAX_LENGTH

    sample_length = min(str_length, SAMPLE_MAX_LENGTH)
    sample = string[:sample_length]

    for shift in range(1, ALPHABET_LENGTH):
        shifted_sample = shift_letters(sample, shift)
        negative_shift = ALPHABET_LENGTH - shift
        message = f'+{shift}/-{negative_shift}:  {shifted_sample}'
        if should_print_ellipsis:
            message += '...'
        print(message)


def decrypt_caesar(string: str):
    sample_caesar(string)
    valid_shift = int(input('Valid shift >> '))
    print(SEPARATOR)
    return shift_letters(string, valid_shift)


def decrypt_binary(string: str):
    string = ''.join(string.split())
    result = []
    for char in chunks(string, 8):
        ascii = chr(int(char, 2))
        result += ascii
    return ''.join(result)


def decrypt_hexadecimal(string: str):
    string = ''.join(string.split())
    return binascii.unhexlify(string).decode()


def decrypt_morse(string: str):
    result = []
    words = string.split(' ')
    for word in words:
        decrypted = MORSE.get(word, '')
        if not decrypted:
            raise ValueError('Word is not a valid morse word.')
        result += decrypted
    return ''.join(result)


def get_command():
    # Print all modes
    for mode in Mode:
        print(f'{mode.value} - {mode.name.capitalize()}.')
    print(f'{EXIT_COMMANDS_JOINED} - Cancel and exit.')
    print(f'{NEW_MESSAGE_COMMAND} - Enter new message.')
    cin = input('>> ')
    return cin


def get_message():
    cin = input('Message to decipher >> ')
    while not cin or cin.isspace():
        cin = input('Message to decipher >> ')
    return cin


def welcome():
    print('*=*=* Secret Message Decoder v1.0.0 *=*=*')
    print('By Alexander Laptev, 2021.')
    print(SEPARATOR)


def decrypt(string: str, mode: Mode):
    decrypted = None
    if mode == Mode.ATBASH:  # Had to replace match/case to make it work with Python older than 3.10.
        decrypted = decrypt_atbash(string)
    elif mode == Mode.CAESAR:
        decrypted = decrypt_caesar(string)
    elif mode == Mode.BINARY:
        try:
            decrypted = decrypt_binary(string)
        except ValueError:
            print('!!! Invalid binary !!!')
            return None
    elif mode == Mode.HEXADECIMAL:
        try:
            decrypted = decrypt_hexadecimal(string)
        except binascii.Error:
            print('!!! Invalid hex !!!')
            return None
    elif mode == Mode.MORSE:
        try:
            decrypted = decrypt_morse(string)
        except ValueError:
            print('!!! Invalid morse !!!')
            return None

    return decrypted


# The main loop.
welcome()
message = get_message()

while True:
    print(SEPARATOR)
    cmd = get_command()
    print(SEPARATOR)

    if cmd in EXIT_COMMANDS:
        break
    elif cmd == NEW_MESSAGE_COMMAND:
        message = get_message()
    else:
        try:
            mode = Mode(int(cmd))
        except ValueError:
            print('Invalid mode.')
            continue

        decrypted = decrypt(message, mode)
        if decrypted is None:
            print("!!! Couldn't decrypt the message !!!")
        else:
            print(f'RESULT: {decrypted}')
