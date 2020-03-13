import json
import requests
import os
import pytesseract
from io import BytesIO
from PIL import Image
import sys

IMAGES_URL = "http://s0urce.io/client/img/word/{key}/{value}"
MAIN_URL = "http://s0urce.io"
FILE_IMAGES = "hackergame_images"
order = {"e": 62, "m": 66, "h": 55}

# If you don't have tesseract executable in your PATH, include the following:
# TESSERACT_EXECUTABLE_PATH = r'<full_path_to_your_tesseract_executable>
TESSERACT_EXECUTABLE_PATH = None
# In my case is r'C:\Program Files\Tesseract-OCR\tesseract.exe

__all__ = ("start",)

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


def create_files():
    """Creating files of Images"""
    if not os.path.exists(FILE_IMAGES):
        os.mkdir(FILE_IMAGES)
        for keys in order.keys():
            try:
                os.mkdir(os.path.join(FILE_IMAGES, keys))
            except FileExistsError:
                print("FileExistsError")
                sys.exit(1)
        return True
    else:
        return False


def download_images():
    """Downloading images"""
    if create_files():
        print("[*] Download Images, Please Wait...")
        for keys, values in order.items():
            for value in range(values):
                data = requests.get(IMAGES_URL.format(key=keys, value=value))
                if data.status_code == 200:
                    images = Image.open(BytesIO(data.content))
                    images.save(os.path.join(os.path.join(FILE_IMAGES, keys), "{}{}.png".format(keys, value)))
        return search_and_edit_images()


def ocr_image(IM):
    """Recognize Text"""
    if TESSERACT_EXECUTABLE_PATH is not None:
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXECUTABLE_PATH
    word = pytesseract.image_to_string(Image.open(IM))
    return word.lower()


def _edit_image(image, size=None):
    """Editing images for text recognition"""
    if size is not None:
        pensize = Image.open(image)
        im = pensize.convert("RGB").resize((300, size))
    else:
        im = Image.open(image).convert("RGB")

    new = Image.new("RGB", (im.width, im.height))
    for i in range(im.width):
        for j in range(im.height):
            r, g, b = im.getpixel((i, j))
            if r == g:
                new.putpixel((i, j), (0, 0, 0))
            else:
                new.putpixel((i, j), (255, 255, 255))
    new.save("digital.png")
    return "digital.png"


def search_and_edit_images():
    print("[+] editing images, please wait...".title())
    word_dictionary = {}

    for root, dirs, files in os.walk(FILE_IMAGES):
        for filenames in files:
            if filenames.endswith(".png"):

                picture_path = os.path.join(root, filenames)
                processing_image = _edit_image(picture_path)
                image_to_word = ocr_image(processing_image)

                if image_to_word not in ALL_WORDS:
                    size = 20

                    while image_to_word not in ALL_WORDS:
                        processing_image = _edit_image(picture_path, size=size)
                        image_to_word = ocr_image(processing_image)
                        size += 5
                        if size > 200:
                            word_dictionary[filenames] = None
                            break
                    else:
                        word_dictionary[filenames] = image_to_word
                else:
                    word_dictionary[filenames] = image_to_word

    with open("wordlist.txt", "w") as f:
        json.dump(word_dictionary, f, indent=4)
    try:
        os.remove("digital.png")
        print("[!] Done!")
        sys.exit(1)
    except Exception as e:
        print(str(e))
        pass


def start():
    download_images()
