# sourceioBot
A Βot that runs automatically and plays for you

# Requirements

To run this script you need to install the following packages:

- [Selenium](https://selenium-python.readthedocs.io/)

- [pytesseract](https://pypi.org/project/pytesseract/)

- [Pillow](https://pillow.readthedocs.io/en/stable/installation.html)

or via **pip**

```pip3 install selenium```

```pip3 install pytesseract```

```pip3 install Pillow```

For selenium you need to download [chromedriver.exe](https://chromedriver.chromium.org/)
If you don't have **chromedriver.exe** in your PATH, open the ```sourceioBot.py``` and pass the full path in the variable **CHOMEDRIVER_PATH** 

```CHOMEDRIVER_PATH = "r'<full_path_to_your_chromedriver.exe>```

Also, you will need the **tesseract.exe**

1. If you are using windows OS you have to install tesseract-ocr from [here](https://github.com/UB-Mannheim/tesseract/wiki)

2. If you are using Ubuntu - in terminal type ```sudo apt-get install tesseract-ocr```

If you don't have tesseract executable in your PATH, open the ```training.py``` and put the full path of the **tesseract.exe** in the variable **TESSERACT_EXECUTABLE_PATH**  

```TESSERACT_EXECUTABLE_PATH = r'<full_path_to_your_tesseract_executable>``` 

In my case is 

```TESSERACT_EXECUTABLE_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe```


# How to use

After you have done the above, 
In your terminal just type ```python3 sourceioBot.py --username <some username> -S -U``` 

**Note** s0urceio is updating the images order everyday. `-U` is for update.

It will stop when all images downloaded.
It has 100% image recognition
In the game open **My Computer**
Enjoy!


