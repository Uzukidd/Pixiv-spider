import json
from urllib.parse import urlencode
from PIL import Image
from WebCraw.Utils import WebRequest
from Data_Struct import Arkwork

class LastestPicGetter :

    STANDARD_URL_TEMPLATE = "https://www.pixiv.net/touch/ajax/search/illusts?include_meta=1&s_mode=s_tag&type=all"

    MODE = {
        "r18", "safe"
    }

    TYPE = {
        "manga", 
        "illustrations", 
        "novels"
    }

    def __init__(self, keyword:str, mode:str = None, cookie:str = "", UA:str = "", proxies:dict = {}) :

        self.keyword = keyword
        self.request_current = None
        self.json = None
        self.cookie = cookie
        self.UA = UA
        self.proxies = proxies
        self.mode = mode
        self.artworks = []


    def request(self, page:int) -> None:
        arg = {
            "p":page,
            "word":self.keyword
        }
        if self.mode == "r18" or self.mode == "safe" :
            arg["mode"] = self.mode
        
        arg_encode = urlencode(arg)
        self.request_current = WebRequest.get(LastestPicGetter.STANDARD_URL_TEMPLATE + "&" + arg_encode, headers = {
            'User-Agent': self.UA, 
            "cookie" : self.cookie
                    }, proxies = self.proxies)

        self.json = json.loads(self.request_current.text)
        self.request_current.close()


def main() :

    COOKIE = ""
    # Use Your cookie if you want to login.
    try : 
        with open("COOKIE.key") as ios:
            COOKIE = ios.readline()
    except :
        pass

    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    PROIXES = {"http":"socks5://127.0.0.1:10808", 
    "https":"socks5://127.0.0.1:10808"}

    keyword = "艦これ 卯月"
    mode = None

    picker = LastestPicGetter(keyword,
    cookie = COOKIE,
    UA = UA, 
    proxies = PROIXES)

    for i in range(1, 2) :

        picker.request(i)

        for illust in picker.json['body']['illusts'] :
            if('id' in illust) : 
                print(illust['id'])
                artwork = Arkwork(illust['id'], cookie = COOKIE,
                UA = UA, 
                proxies = PROIXES)
                artwork.request()
                print("pages:%d" % artwork.page_count)
                print("type:" + artwork.type)

                artwork.download_path("pics\\")

                # print(artwork.src["original"])
            else : print("None Id")

if __name__ == "__main__":
    main()

    

