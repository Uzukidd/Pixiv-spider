import json
import requests
import os

try:
    from .Web_Craw.Utils import WebRequest
    from .Utils import zip2gif, extract_zip
except ImportError:
    from Web_Craw.Utils import WebRequest
    from Utils import zip2gif, extract_zip

class Image_Set :

    QUALITY = {
        "small", 
        "medium",
        "origin"
    }

    def __init__(self, small, medium, origin):

        self.images = {
            "small" : small,
            "medium" : medium,
            "origin" : origin
        }


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
        self.ugoira_durations = []
        self.is_ugoira = False
        self.cookie = cookie
        self.UA = UA
        self.proxies = proxies

    def request(self) -> None :

        self.request_current = WebRequest.get(Arkwork.STANDARD_URL_TEMPLATE % self.id, headers = {
            'User-Agent': self.UA, 
            "cookie" : self.cookie
                    }, proxies = self.proxies)

        self.json = json.loads(self.request_current.text)

        # If any errors
        if self.json["error"] :
            print(self.json["message"])
            return

        # Parsing the json
        self.src = self.json["body"]
        self.detail = self.src["illust_details"]
        self.page_count = int(self.detail["page_count"])
        self.images.clear()

        # If it's a manga (comic)
        if "manga_a" in self.detail : 
            self.type = "manga"
            for image in self.detail["manga_a"] :
                self.images.append(Image_Set(image["url_small"], 
                image["url"], 
                image["url_big"]))

        else :
            # If it's an illustration
            self.type = "illust"

            # If it's an ugoira (animation)
            if self.detail["ugoira_meta"] is None :
                self.is_ugoira = False
                self.images.append(Image_Set(self.detail["url_placeholder"], 
                self.detail["url"], 
                self.detail["url_big"]
                ))

            else :
                self.is_ugoira = True
                self.images.append(Image_Set(None, 
                None, 
                self.detail["ugoira_meta"]["src"]))

                durations_temp = []
                for frame in self.detail["ugoira_meta"]["frames"] :
                    # Unit conversion (ms -> s)
                    durations_temp.append(frame["delay"] * 0.001)
                self.ugoira_durations.append(durations_temp)

        self.request_current.close()

    def has_requested(self) -> bool:
        return self.json is not None

    def download(self, pages = None, quality = "origin") -> bytes :
        assert self.has_requested()

        headers = {
            'User-Agent':self.UA, 
            'Referer' : Arkwork.STANDARD_URL_TEMPLATE % self.id, 
            "cookie" : self.cookie
        }

        assert quality in Image_Set.QUALITY

        # None means all
        if pages is None: 
            pages = range(0, self.page_count)

        for page in pages :
            pic = None
            while(pic is None or pic.status_code != 200) :
                try:
                    pic = requests.get(self.images[page].images[quality], timeout = 100, headers = headers, proxies = self.proxies)
                except requests.exceptions.ConnectionError:
                    return
            
            yield (pic.content, page)
            pic.close()

        
    def download_path_gif(self, path:str) -> None:
        assert self.has_requested()
        assert self.is_ugoira

        for image, page in self.download([0]) :
        
            dir = os.path.join(path, self.id+ ".gif")

            if(not os.path.exists(path)) : 
                os.mkdir(path)

            fp = open(dir, 'wb')
            fp.write(zip2gif(image, self.ugoira_durations[0]))
            fp.close()

    def download_path(self, path:str, pages = None) -> None:
        assert self.has_requested()

        if pages is None: 
            pages = range(0, self.page_count)

        if self.type == "manga" :
            path = os.path.join(path , self.id)

        for image, page in self.download(pages) :
            
            if self.type == "manga" :
                dir = os.path.join(path , self.id+ "_p%d.png" % page)
            elif self.type == "illust" :
                if self.is_ugoira :
                    dir = os.path.join(path, self.id)
                else :
                    dir = os.path.join(path, self.id+ ".png")

            if(not os.path.exists(path)) : 
                os.mkdir(path)
            
            # If it's an ugoira (animation)
            if(self.is_ugoira and not os.path.exists(dir)) :
                os.mkdir(dir)

            if not self.is_ugoira :
                fp = open(dir, 'wb')
                fp.write(image)
                fp.close()
            else:
                for img, name in extract_zip(image) :
                    fp = open(os.path.join(dir, name), 'wb')
                    fp.write(img)
                    fp.close()
                

            

def main() -> None :
    # Generally, cookie is no need when downloading an r18 artwork instead of searching
    COOKIE = ""

    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    
    PROIXES = {"http":"socks5://127.0.0.1:10808", 
    "https":"socks5://127.0.0.1:10808"}

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