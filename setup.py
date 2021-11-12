from setuptools import setup, find_packages

setup(
    name = "Pixiv Web Crawler",
    version = "1.1.0",
    # keywords = (),
    # description = "eds sdk",
    # long_description = "eds sdk for python",
    license = "MIT Licence",

    # url = "http://test.com",
    author = "Uzuki",
    author_email = "uzukidd@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [""],

    scripts = [],
    entry_points = {
        'console_scripts': [
            'test = test.help:main'
        ]
    }
)