from typing import Tuple, Optional
import PIL
import requests
from PIL import Image
import pytesseract
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from difflib import SequenceMatcher
import json
import time

# If you don't have tesseract executable in your PATH, include the following:
# TESSERACT_EXECUTABLE_PATH = r'<full_path_to_your_tesseract_executable>
TESSERACT_EXECUTABLE_PATH = None
# In my case is r'C:\Program Files\Tesseract-OCR\tesseract.exe

ALL_WORDS = ['get', 'add', 'dir', 'list', 'file', 'ghost', 'http', 'pass', 'ping', 'port', 'write', 'remove', 'anon',
             'user', 'bytes', 'socket', 'net', 'val', 'count', 'point', 'event', 'reset', 'com', 'signal', 'load',
             'handle', 'key', 'stat', 'buffer', 'send', 'host', 'delete', 'bit', 'size', 'upload', 'poly', 'temp',
             'system', 'root', 'client', 'data', 'init', 'info', 'xml', 'log', 'loop', 'global', 'cookies', 'part',
             'emit', 'set', 'url', 'call', 'type', 'add', 'left', 'join', 'status', 'right', 'num', 'domain', 'intel',
             'constructor', 'encryptfile', 'getpass', 'responder', 'setstats', 'encrypt', 'newline', 'mysql',
             'writefile', 'eventtype', 'accountname', 'download', 'setcookie', 'setnewid', 'command', 'thread',
             'process', 'listconfig', 'syscall', 'proxy', 'filedir', 'newhost', 'getid', 'server', 'number', 'sizeof',
             'module', 'urlcheck', 'gridwidth', 'decrypt', 'datatype', 'config', 'getinfo', 'userport', 'hostserver',
             'account', 'generate', 'filetype', 'decryptfile', 'setport', 'threat', 'package', 'userid', 'loadbytes',
             'channel', 'hexagon', 'disconnect', 'getfile', 'encode', 'protocol', 'password', 'getkey', 'serverproxy',
             'gridheight', 'getping', 'getlog', 'export', 'connect', 'newserver', 'findpackage', 'length', 'vector',
             'fillgrid', 'username', 'response', 'setping', 'joinnetworkclient', 'unpacktmpfile', 'getdatapassword',
             'bufferpingset', 'emitconfiglist', 'rootcookieset', 'setnewproxy', 'sizeofhexagon', 'getmysqldomain',
             'callmodule', 'getfirewallchannel', 'changeusername', 'httpbuffersize', 'removeoldcookie',
             'fileexpresslog', 'getpartoffile', 'disconnectserver', 'batchallfiles', 'exportconfigpackage',
             'statusofprocess', 'getxmlprotocol', 'loadloggedpassword', 'sendintelpass', 'eventlistdir',
             'changepassword', 'uploaduserstats', 'decryptdatabatch', 'loadregisterlist', 'systemgridtype',
             'encodenewfolder', 'encryptunpackedbatch', 'destroybatch', 'dodecahedron', 'respondertimeout',
             'channelsetpackage', 'checkhttptype', 'tempdatapass', 'blockthreat', 'deleteallids', 'removenewcookie',
             'ghostfilesystem', 'includedirectory', 'create3axisvector', 'systemportkey', 'mergesocket',
             'patcheventlog', 'createnewpackage', 'disconnectchannel', 'createfilethread', 'wordcounter',
             'create2axisvector', 'generatecodepack', 'createnewsocket', 'hostnewserver', 'loadaltevent']


class Recognition:
    def __init__(self, image: PIL.Image, file_name: str = '') -> None:
        self.image = image
        self.file_name = file_name

    @classmethod
    def read_from_url(cls, url: str) -> 'Recognition':
        """Reading the image link creates a folder with the image name and saves it"""

        """From the following link for example "http://s0urce.io/client/img/word/m/1" we get the last two items """
        image_name = url.split('/')[-2:]  # ['m','1']

        folder_path = Path(f'images/{image_name[0]}')
        folder_path.mkdir(parents=True, exist_ok=True)

        with requests.get(url) as response:
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            filename = f'{"".join(image_name)}.png'
            img.save(folder_path / filename)
        return cls(img, filename)

    def edit_image(self, size: Optional[Tuple] = None) -> PIL.Image:
        """Clean the image and turn all the colors to white except the letters
        Args:
            size (Optional[Tuple], optional): [description]. Defaults to None.

        Returns:
            PIL.Image: Edited image
        """
        image = self.image.convert(('RGB'))
        edited_image = Image.new('RGB', (image.width, image.height))
        for i in range(image.width):
            for j in range(image.height):
                r, g, _ = image.getpixel((i, j))
                if r == g:
                    edited_image.putpixel((i, j), (0, 0, 0))
                else:
                    edited_image.putpixel((i, j), (255, 255, 255))
        if size is not None:
            return edited_image.resize(size)
        return edited_image

    def get_image_text(self) -> str:
        """With the help of pytesseract we get the word of image and match it with ALL_WORDS
         If necessary, resize the image

        Returns:
            str: Word of Image
        """
        img = self.edit_image()
        if TESSERACT_EXECUTABLE_PATH is not None:
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXECUTABLE_PATH
        fetch_word = pytesseract.image_to_string(img).strip()
        ratio, word = max(
            [(SequenceMatcher(None, fetch_word, w).ratio(), w) for w in ALL_WORDS])
        while ratio <= 0.75:
            x, _ = size = (200, 100)
            img = self.edit_image(size)
            
            fetch_word = pytesseract.image_to_string(img).strip()
            ratio, word = max(
                [(SequenceMatcher(None, fetch_word, w).ratio(), w) for w in ALL_WORDS])
            x += 50
            if x > 1000:
                break

        return word.lower()


def create_wordlist() -> None:
    """The final result is the wordlist
    """

    ORDER = {"e": 62, "m": 66, "h": 55}
    BASE_URL = "http://s0urce.io/client/img/word/{key}/{value}"

    urls = [
        BASE_URL.format(key=key, value=value) for key, values in ORDER.items() for value in range(values)
    ]
    words = {}
    print('[!] Please wait...')
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = [executor.submit(Recognition.read_from_url, url)
                   for url in urls]
        for res in as_completed(results):
            filename = res.result().file_name
            word = Recognition(res.result().image).get_image_text()
            words[filename] = word

    with open('wordlist.json', 'w') as f:
        json.dump(words, f, indent=4)

    print('[*] Images and WordList are ready...')


def nulls_in_wordlist() -> bool:
    with open('wordlist.json', 'r') as f:
        content = json.load(f)

    nulls = [key for key, value in content.items() if value is None]

    if nulls:
        print('[!] Please fill the empty fields on wordlist.json')
        print('\n'.join(nulls))
        return True
    return False



