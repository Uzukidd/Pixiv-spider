import json
import requests
import os
import io
import zipfile
try:
    from .Web_Craw.Utils import WebRequest
except ImportError:
    from Web_Craw.Utils import WebRequest

class Arkwork :

    STANDARD_URL_TEMPLATE = "https://www.pixiv.net/touch/ajax/illust/details?illust_id=%s&ref="

    STANDARD_HEADER_TEMPLATE = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36', 
    }

    TYPE = [
        "manga",
        "illust"
    ]


    def __init__(self, id:str, cookie:str = "", UA:str = "", proxies:dict = {}) :

        self.id = id
        self.src = None
        self.request_current = None
        self.json = None
        self.detail = None
        self.type = ""
        self.page_count = -1
        self.images = []
        self.ugoira_zip = []
        self.is_ugoira = False
        self.cookie = cookie
        self.UA = UA
        self.proxies = proxies

    def request(self) :

        self.request_current = WebRequest.get(Arkwork.STANDARD_URL_TEMPLATE % self.id, headers = {
            'User-Agent': self.UA, 
            "cookie" : self.cookie
                    }, proxies = self.proxies)

        self.json = json.loads(self.request_current.text)

        if self.json["error"] :
            print(self.json["message"])
            return

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
            if self.detail["ugoira_meta"] is None :
                self.is_ugoira = False
                self.images.append(self.detail["url_big"])
            else :
                self.is_ugoira = True
                self.images.append(self.detail["ugoira_meta"]["src"])

        self.request_current.close()

    def has_requested(self) -> bool:
        return self.json is not None

    def download_path(self, path:str, pages = None) -> None:
        assert self.has_requested()

        pic = None

        headers = {
            'User-Agent':self.UA, 
            'Referer' : Arkwork.STANDARD_URL_TEMPLATE % self.id, 
            "cookie" : self.cookie
        }

        if pages is None: 
            pages = range(0, self.page_count)

        for page in pages :
            while(pic == None or pic.status_code != 200) :
                try:
                    pic = requests.get(self.images[page], timeout = 100, headers = headers, proxies = self.proxies)
                except requests.exceptions.ConnectionError:
                    return
            
            if self.type == "manga" :
                dir = os.path.join(path, self.id+ "_p%d.png" % page)
            elif self.type == "illust" :
                if self.is_ugoira :
                    dir = os.path.join(path, self.id)
                else :
                    dir = os.path.join(path, self.id+ ".png")

            if(not os.path.exists(path)) : 
                os.mkdir(path)

            if not self.is_ugoira :
                fp = open(dir, 'wb')
                fp.write(pic.content)
                fp.close()
            else:
                buffer = io.BytesIO(initial_bytes = pic.content)
                zip_file = zipfile.ZipFile(file = buffer)
                for file_name in zip_file.namelist():
                    zip_file.extract(file_name, dir)
                zip_file.close()
                

            pic.close()
            pic = None

            

def main() -> None :
    COOKIE = ""
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    PROIXES = {"http":"socks5://127.0.0.1:10808", 
    "https":"socks5://127.0.0.1:10808"}
    artwork = Arkwork("91712657", 
    cookie = COOKIE,
    UA = UA, 
    proxies = PROIXES)
    artwork.request()
    print("pages:%d" % artwork.page_count)
    print("type:" + artwork.type)
    print("Image:", artwork.images)
    # print(artwork.json)
    artwork.download_path("pics\\")

if __name__ == "__main__" :
    main()