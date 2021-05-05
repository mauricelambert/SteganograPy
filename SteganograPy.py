#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This package hide text or bytes in image.
#    Copyright (C) 2021  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

""" This package hide text or bytes in image. """

from base64 import b85decode, b85encode
from gzip import compress, decompress
from argparse import ArgumentParser
from typing import TypeVar
from PIL import Image
from os import path

__version__ = "0.0.1"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__url__ = 'https://github.com/mauricelambert/SteganograPy'

__description__ = "This package hide text or bytes in image."
__license__ = "GPL-3.0 License"
copyright = """
SteganograPy  Copyright (C) 2021  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
license = __license__
__copyright__ = copyright

print(copyright)

__all__ = ["SteganoError", "Stegano"]

StringOrBytes = TypeVar("StringOrBytes", str, bytes)
base85_chars = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+-;<=>?@^_`{|}~"


class SteganoError(Exception):

    """This class raise SteganoError."""

    pass


class Stegano:

    """This class hide text or bytes in image."""

    def __init__(
        self,
        filename: str,
        message: StringOrBytes = None,
        color: str = "red",
        output_file: str = None,
    ):
        self.color = color
        self.new_image = None
        self.filename = filename

        if message is not None:
            self.message = b85encode(
                compress(message.encode() if isinstance(message, str) else message)
            )

        if output_file is None:
            self.output_file = f"{path.splitext(path.basename(filename))[0]}_stegano.png"
        else:
            self.output_file = f"{path.splitext(path.basename(output_file))[0]}.png"

        self.set_image()

    def set_image(self) -> None:

        """This function open the picture, get size,
        get colors and filter."""

        self.image = Image.open(self.filename)
        self.image = self.image.convert("RGB")
        self.width, self.height = self.image.size
        self.red, self.green, self.blue = self.image.split()
        self.filter = self.get_filter()

    def get_filter(self) -> list:

        """Return a list of pixels (red, green or blue) or
        raise a SteganoError."""

        if self.color == "red":
            return list(self.red.getdata())
        elif self.color == "green":
            return list(self.green.getdata())
        elif self.color == "blue":
            return list(self.blue.getdata())
        else:
            raise SteganoError(
                f'Color error ({self.color} is not "red", "green" or "blue").'
            )

    def stegano(self) -> list:

        """This function build filter with hidden text."""

        length = len(self.message)
        binary_length = bin(length if length < 255 else 255)[2:].rjust(8, "0")

        length = length * 8
        if length > len(self.filter):
            raise SteganoError("Length of encoded data x8 is larger than image size.")

        binary_message = "".join([bin(x)[2:].rjust(8, "0") for x in self.message])

        for i in range(8):
            number = self.filter[i] if not (self.filter[i] % 2) else self.filter[i] - 1
            self.filter[i] = number + int(binary_length[i])

        for i in range(length):
            number = self.filter[i] if not (self.filter[i] % 2) else self.filter[i] - 1
            self.filter[i + 8] = number + int(binary_message[i])

        return self.filter

    def build_and_save_new_image(self) -> None:

        """This function build the new image with hidden text
        and write it."""

        self.filter = self.stegano()

        change = Image.new("L", (self.width, self.height))
        change.putdata(self.filter)

        if self.color == "red":
            self.new_image = Image.merge("RGB", (change, self.green, self.blue))
        elif self.color == "green":
            self.new_image = Image.merge("RGB", (self.red, change, self.blue))
        elif self.color == "blue":
            self.new_image = Image.merge("RGB", (self.red, self.green, change))
        else:
            self.new_image = Image.merge("P", [change])

        self.new_image.save(self.output_file)

    def get_message(self) -> bytes:

        """This function get message from image."""

        length_binary_value = "".join([str(x % 2) for x in self.filter[0:8]])
        length = (
            int(length_binary_value, 2)
            if length_binary_value != "11111111"
            else len(self.filter) // 8
        )  # size is write if size of message is smaller than 255 characters

        binary_message = "".join(
            [str(x % 2) for x in self.filter[8:8 * (length + 1)]]
        )

        message = []
        for k in range(length):
            binary_char = binary_message[8 * k:8 * k + 8]
            char = int(binary_char, 2)
            if char in base85_chars:
                message.append(char)
            else:
                break

        self.message = decompress(b85decode(bytes(message)))
        return self.message


def parse_args():

    """This function parse command line arguments."""

    parser = ArgumentParser()
    parser.add_argument("imagename", help="Image filename")
    parser.add_argument("-m", "--message", help="Message to hide.")
    parser.add_argument(
        "-d", "--decode", help="Get message from image.", action="store_true"
    )
    parser.add_argument(
        "-c",
        "--color",
        help="Color to use to hide/get data.",
        choices=["green", "red", "blue"],
        default="red",
    )
    parser.add_argument("-f", "--file", help="Filename to get data.")
    parser.add_argument("-o", "--output-file", help="Filename to write image.")
    return parser.parse_args()


def main() -> None:

    """Main function for command line."""

    args = parse_args()
    stegano = Stegano(
        args.imagename,
        message=args.message,
        color=args.color,
        output_file=args.output_file,
    )
    if args.decode:
        print(stegano.get_message().decode())

    elif args.message or args.file:
        if args.file:
            with open(args.file, "rb") as file:
                args.message = file.read()
        else:
            args.message = args.message.encode()

        stegano.message = b85encode(compress(args.message))
        stegano.build_and_save_new_image()
    else:
        print(
            "One of the following arguments is required:"
            " -d/--decode, -m/--message or -f/--file"
        )
        exit(1)


if __name__ == "__main__":
    main()
