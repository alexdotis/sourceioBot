# sourceioBot
A Βot that runs automatically and plays for you

# Requirements

To run this script you need to have the following packages:

- [Selenium](https://selenium-python.readthedocs.io/)

[pytesseract](https://pypi.org/project/pytesseract/)

[Pillow](https://pillow.readthedocs.io/en/stable/installation.html)

```pip install selenium```

```pip install pytesseract```

```pip install Pillow```

For selenium you need to download [chromedriver.exe](https://chromedriver.chromium.org/)
If you don't have **chromedriver.exe** in your PATH, open the ```sourceioBot.py``` and pass the full path in the variable **CHOMEDRIVER_PATH** 

```CHOMEDRIVER_PATH = "r'<full_path_to_your_chromedriver.exe>```

Also, you will need the **tesseract.exe**

1. If you are using windows OS you have to install tesseract-ocr from [here](https://github.com/UB-Mannheim/tesseract/wiki)

2. If you are using ubuntu OS - in terminal type ```sudo apt-get install tesseract-ocr```

If you don't have tesseract executable in your PATH, open the ```extract_images.py``` and put the full path of the **tesseract.exe** in the variable **TESSERACT_EXECUTABLE_PATH**  

```TESSERACT_EXECUTABLE_PATH = r'<full_path_to_your_tesseract_executable>``` 

In my case is 

```TESSERACT_EXECUTABLE_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe```


# How to use

After you have done the above, put your username in the variable **USERNAME** in ```sourceioBot.py``` in the end of code and run it.
It will stops when all images downloaded.
It has 100% for image recognition but, just in case check in the **wordlist.txt** if some words are missing and fill them.
Run it again! 
In the game open **My Computer**
Enjoy!


