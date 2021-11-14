from setuptools import setup, find_packages

setup(
    name = "Pixiv-Spider",
    version = "1.1.5",
    license = "MIT",
    description='Implementation of Pixiv Web Spider',
    url = "https://github.com/Uzukidd",
    download_url = "https://github.com/Uzukidd/Pixiv-web-crawler", 
    author = "Uzukidd",
    author_email = "uzukidd@gmail.com",
    install_requires=['tqdm',
                'requests',
                'imageio',
                'zipfile'
                ],

    packages = find_packages()

)