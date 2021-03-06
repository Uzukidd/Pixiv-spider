# Pixiv-spider
A Pixiv spider module

## Features

0006 -

​	Now choosing different qualities of a artwork supported, bugs fixed.

0005 -

​	Now parsing a ugoira (animation) is supported, bugs fixed.

0004 -

​	Readme.md updated, comments fixed, variable names fixed.

0003 -

​	Name changed to \"Pixiv-spider\", bugs fixed, ugoira added.

## Requirements

tqdm

requests

imageio

zipfile

## Installation

Clone or download this repository than get into it and input this on your terminal:

```
python ./setup.py install
```

## Usage

classes

- LastestPicGetter -  Picker to get the lastest artworks by get method
- Artwork - Format to request and parse artworks

## Example

```python
from pixiv_spider.Getters import LastestPicGetter


def main() :

    COOKIE = ""
    # Use Your cookie if you want to login.
    try : 
        with open("./COOKIE.key") as ios:
            COOKIE = ios.readline()
    except :
        print("COOKIE.key not found")

    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    # User-Agent
    
    # PROIXES = {"http":"socks5://127.0.0.1:10808", 
    # "https":"socks5://127.0.0.1:10808"}
    
    PROIXES = None
    # Proxies if needed

    keyword = "艦これ"
    # Keyword for searching
    
    mode = "safe" #"r18" or "safe"
    # Logging in is necessary if using R-18 mode

    picker = LastestPicGetter(keyword, mode = mode,
    cookie = COOKIE,
    UA = UA, 
    proxies = PROXIES)
    # Create a picker by get method
	
    # Download images from page 1 to page 2
    for i in range(1, 3) :

        picker.request(i)
        picker.parsing()

        print("Result:", list(picker.result.keys()))
        print("Last page:", picker.last_page)

        picker.download_path_all(".\\pics\\")

if __name__ == "__main__":
    main()
```

```python
from pixiv_spider.Data_Struct import Arkwork

def main() -> None :
    
    COOKIE = ""
    # Generally, there is no need for cookie to download an r18 artwork instead of search

    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    
    # PROIXES = {"http":"socks5://127.0.0.1:10808", 
    # "https":"socks5://127.0.0.1:10808"}
    
    PROIXES = None
    # Proxies if needed

    test_id = [
        "91712657", # ugoira(r18)
        # "88826080", # ugoira
        "93615483", # manga
        "93470614"  # illust
    ]

    for i in test_id :
        artwork = Arkwork(i, 
        cookie = COOKIE,
        UA = UA, 
        proxies = PROIXES)
        artwork.request()

        print("id:", artwork.id)
        print("pages:%d" % artwork.page_count)
        print("type:" + artwork.type)
        print("Image:", artwork.images)

        if artwork.is_ugoira : artwork.download_path_gif("pics\\")

        artwork.download_path("pics\\")

if __name__ == "__main__" :
    main()
```



# MIT License

Copyright (c) 2021 Uzuki



Permission is hereby granted, free of charge, to any person obtaining a copy

of this software and associated documentation files (the "Software"), to deal

in the Software without restriction, including without limitation the rights

to use, copy, modify, merge, publish, distribute, sublicense, and/or sell

copies of the Software, and to permit persons to whom the Software is

furnished to do so, subject to the following conditions:



The above copyright notice and this permission notice shall be included in all

copies or substantial portions of the Software.



THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR

IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,

FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE

AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER

LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,

OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE

SOFTWARE.
