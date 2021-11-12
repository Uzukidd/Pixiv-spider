import json
import requests
import os
from WebCraw.Utils import WebRequest

class Arkwork :

    STANDARD_URL_TEMPLATE = "https://www.pixiv.net/touch/ajax/illust/details?illust_id=%s&ref="

    STANDARD_HEADER_TEMPLATE = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36', 
    }


    def __init__(self, id:str, cookie:str = "", UA:str = "", proxies:dict = {}) :

        self.id = id
        self.src = None
        self.request_current = None
        self.json = None
        self.detail = None
        self.type = ""
        self.page_count = -1
        self.images = []
        self.cookie = cookie
        self.UA = UA
        self.proxies = proxies

    def request(self) :

        self.request_current = WebRequest.get(Arkwork.STANDARD_URL_TEMPLATE % self.id, headers = {
            'User-Agent': self.UA, 
            "cookie" : self.cookie
                    }, proxies = self.proxies)

        self.json = json.loads(self.request_current.text)

        self.src = self.json["body"]
        self.detail = self.src["illust_details"]
        self.page_count = int(self.detail["page_count"])
        self.images.clear()

        if "manga_a" in self.detail : 
            self.type = "manga"
            for image in self.detail["manga_a"] :
                self.images.append(image["url_big"])
        else :
            self.type = "illust"
            self.images.append(self.detail["url_big"])

        self.request_current.close()

        # print(self.json["body"])

    def download_path(self, path:str, pages = None):

        pic = None

        headers = {
            'User-Agent':self.UA, 
            'Referer' : Arkwork.STANDARD_URL_TEMPLATE % self.id, 
            "cookie" : self.cookie
        }
        if self.type == "manga" :
            path = path + self.id + "\\"

        if pages is None: 
            pages = range(0, self.page_count)

        for page in pages :
            while(pic == None or pic.status_code != 200) :
                try:
                    print("Try getting:" + self.images[page])
                    pic = requests.get(self.images[page], timeout = 100, headers = headers, proxies = self.proxies)
                except requests.exceptions.ConnectionError:
                    print('图片无法下载')
                    return
            if self.type == "manga" :
                dir = path + self.id+ "_p%d.png" % page
            elif self.type == "illust" :
                dir = path + self.id+ ".png"

            if(not os.path.exists(path)) : os.mkdir(path)

            fp = open(dir, 'wb')
            fp.write(pic.content)
            pic.close()
            pic = None
            fp.close()

def main() -> None :
    COOKIE = ""
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    PROIXES = {"http":"socks5://127.0.0.1:10808", 
    "https":"socks5://127.0.0.1:10808"}
    artwork = Arkwork("94032936", 
    cookie = COOKIE,
    UA = UA, 
    proxies = PROIXES)
    artwork.request()
    print("pages:%d" % artwork.page_count)
    print("type:" + artwork.type)
    # artwork.download_path("pics\\")

if __name__ == "__main__" :
    main()