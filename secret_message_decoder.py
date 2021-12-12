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

# A CLI decoder for secret messages. Created mainly for decoding secret messages from Andy's Apple Farm, but may be
# used for any ciphers, I guess.  Morse dict copied from StackOverflow and pretty printed using another short script.

import binascii
from enum import Enum, auto

SEPARATOR = '=' * 24

EDIT_COMMAND = 'edit'
MORSE = {
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
    return ''.join(result)


def shift_letters(string: str, shift: int):
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
    print_ellipsis = str_length > SAMPLE_MAX_LENGTH
    sample_length = min(str_length, SAMPLE_MAX_LENGTH)
    sample = string[:sample_length]
    for shift in range(1, ALPHABET_LENGTH):
        shifted_sample = shift_letters(sample, shift)
        negative_shift = ALPHABET_LENGTH - shift
        message = f'+{shift}/-{negative_shift}:  {shifted_sample}'
        if print_ellipsis:
            message += '...'
        print(message)


def decrypt_caesar(string: str):
    sample_caesar(string)
    valid_shift = int(input('Valid shift >> '))
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
            result += word
            continue
        result += decrypted
    return ''.join(result)


def get_command():
    # Print all modes
    for mode in Mode:
        print(f'{mode.value} - {mode.name.capitalize()}.')
    print(f'{EXIT_COMMANDS_JOINED} - Cancel and exit.')
    print(f'{EDIT_COMMAND} - Edit the message.')
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


def main():
    welcome()
    message = get_message()

    while True:
        print(SEPARATOR)
        cmd = get_command()
        print(SEPARATOR)
        if cmd in EXIT_COMMANDS:
            break
        elif cmd == EDIT_COMMAND:
            message = get_message()
        else:
            try:
                mode = Mode(int(cmd))
            except ValueError:
                print('Invalid mode.')
                continue

            decrypted = None
            match mode:
                case Mode.ATBASH:
                    decrypted = decrypt_atbash(message)
                case Mode.CAESAR:
                    decrypted = decrypt_caesar(message)
                case Mode.BINARY:
                    decrypted = decrypt_binary(message)
                case Mode.HEXADECIMAL:
                    decrypted = decrypt_hexadecimal(message)
                case Mode.MORSE:
                    decrypted = decrypt_morse(message)
            if decrypted is None:
                print("!!! Couldn't decrypt the message !!!")
            print(f'RESULT: {decrypted}')
