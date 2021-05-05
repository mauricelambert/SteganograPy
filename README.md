# SteganograPy

## Description
This package hide text or bytes in image (PNG only).

## Requirements
This package require :
 - python3
 - python3 Standard Library
 - pillow

## Installation
```bash
pip install SteganograPy
```

## Usages

### Command line:
```bash
Stegano -m "My message !" image.jpg
python3 -m SteganograPy -d image_stegano.png
```

### Python script
```python
from SteganograPy import Stegano

Stegano(
    "image.jpg",
    message="My message.",
    color="red",
    output_file=None,
).build_and_save_new_image()

print(Stegano(
    "image_stegano.png",
    message=None,
    color="red",
    output_file=None,
).get_message().decode())
```

## Command line examples

```bash
Stegano -h
Stegano -m "My message !" image.jpg
Stegano -f test.txt -c green -o test.jpg image.jpg
Stegano -d image_stegano.png
Stegano -c green -d image.png
```

## Links
 - [Github Page](https://github.com/mauricelambert/SteganograPy/)
 - [Documentation](https://mauricelambert.github.io/info/python/security/SteganograPy.html)
 - [Python executable](https://mauricelambert.github.io/info/python/security/SteganograPy.pyz)
 - [Pypi package](https://pypi.org/project/SteganograPy/)

## Licence
Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
