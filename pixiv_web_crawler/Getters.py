import json
from urllib.parse import urlencode
from tqdm import tqdm
from .WebCraw.Utils import WebRequest
from .Data_Struct import Arkwork

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
        self.last_page = -1
        self.result = {}


    def has_requested(self) -> bool:
        return self.json is not None

    def request(self, page:int) -> None:
        arg = {
            "p":page,
            "word":self.keyword
        }
        if self.mode in LastestPicGetter.MODE :
            arg["mode"] = self.mode
        
        arg_encode = urlencode(arg)
        self.request_current = WebRequest.get(LastestPicGetter.STANDARD_URL_TEMPLATE + "&" + arg_encode, headers = {
            'User-Agent': self.UA, 
            "cookie" : self.cookie
                    }, proxies = self.proxies)

        self.json = json.loads(self.request_current.text)
        self.request_current.close()

    def analyze(self) -> None:
        assert self.has_requested()

        self.last_page = self.json['body']['lastPage']
        for illust in self.json['body']['illusts'] :
            if 'id' in illust and illust['id'] not in self.result : 
                self.result[illust['id']] = Arkwork(illust['id'], cookie = self.cookie,
                UA = self.UA, 
                proxies = self.proxies)

    def request_all(self) -> None:
        for illust in tqdm(self.result.values()): 
            illust.request()

    def download_path_all(self, path:str) -> None:
        for illust in tqdm(self.result.values()): 
            if not illust.has_requested():
                illust.request()
            
            illust.download_path(path)


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

    keyword = "艦これ"
    mode = "r18" #"r18" or "safe"
    # Logging in is necessary if using R-18 mode

    picker = LastestPicGetter(keyword,
    cookie = COOKIE,
    UA = UA, 
    proxies = PROIXES)

    for i in range(1, 2) :

        picker.request(i)
        picker.analyze()

        print("Result:", list(picker.result.keys()))
        print("Last page:", picker.last_page)

        # picker.request_all()
        picker.download_path_all(".\\pics\\")


        # for illust in picker.json['body']['illusts'] :
        #     if('id' in illust) : 
        #         print(illust['id'])
        #         artwork = Arkwork(illust['id'], cookie = COOKIE,
        #         UA = UA, 
        #         proxies = PROIXES)
        #         artwork.request()
        #         print("pages:%d" % artwork.page_count)
        #         print("type:" + artwork.type)

        #         artwork.download_path("pics\\")

        #         # print(artwork.src["original"])
        #     else : print("None Id")

if __name__ == "__main__":
    main()

    

