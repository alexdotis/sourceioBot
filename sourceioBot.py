from selenium import webdriver
import random
import time
import json
import re
import decimal
from recognition import extract_images

extract_images.start()

#CHOMEDRIVER_PATH = "r'<full_path_to_your_chromedriver.exe>
CHOMEDRIVER_PATH = None

return_values = {"ammount": '$("#window-my-coinamount").text()',
                 "bot_net": '$("#shop-bot-net-value").text()',
                 "quantum": '$("#shop-quantum-server-value").text()',
                 "max_charges": '$("#shop-max-charges").text()',
                 "max_strength": '$("#shop-strength").text()',
                 "max_regen": '$("#shop-regen").text()',
                 "price_max_charges": '$("#shop-firewall-max_charge10-value").text()',
                 "price_shop_strength": '$("#shop-firewall-difficulty-value").text()',
                 "price_shop_regen": '$("#shop-firewall-regen-value").text()'}

clicks = {"quantum": '$("#shop-quantum-server-value").click()',
          "botnet": '$("#shop-bot-net-value").click()',
          "max_charges": '$("#shop-firewall-max_charge10").click()',
          "shop_strength": '$("#shop-firewall-difficulty").click()',
          "shop_regen": '$("#shop-firewall-regen-value").click()'}

firewall_config_charges = {'max_charges': 30, 'max_strength': 4, 'max_regen': 10}


class SourceIoBot:

    def __init__(self, username):
        self.username = username
        self.url = "http://s0urce.io/"
        if CHOMEDRIVER_PATH is not None:
            self.driver = webdriver.Chrome(CHOMEDRIVER_PATH)
        else:
            self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        time.sleep(3)

    def __str__(self):
        return self.username

    def login(self):
        self.driver.find_element_by_id("login-input").send_keys(self.username)
        submit = self.driver.find_element_by_tag_name("form")
        submit.submit()
        time.sleep(2)

    def find_target(self):
        player_list = f'$("#player-list").children("tr")[{int(random.randrange(0, 5))}].click()'
        self.driver.execute_script(player_list)
        self.driver.execute_script('$("#window-other-button").click()')
        self.driver.execute_script('$("#window-other-port{}").click()'.format(random.randrange(1, 3)))
        time.sleep(0.5)

    def attack(self):
        time.sleep(3)
        while True:
            self.find_target()
            progress_bar = self.driver.execute_script('return $("#progressbar-firewall-amount").attr("style")')
            percentage_of_progress_bar = "".join(re.findall(r'[0-9]+', progress_bar))

            while int(percentage_of_progress_bar) <= 100:
                icon = self.driver.find_elements_by_class_name("tool-type-img")
                for image in icon:
                    link = image.get_attribute('src')
                if link == "http://s0urce.io/client/img/words/template.png":
                    break
                image_link = "".join(link.split("/")[6:]) + ".png"
                type_word = find_word(image_link)
                self.driver.execute_script('$("#tool-type-word").val("{}")'.format(type_word))
                self.driver.execute_script('$("#tool-type-word").val("{}").submit()'.format(type_word))
                progress_bar = self.driver.execute_script('return $("#progressbar-firewall-amount").attr("style")')
                percentage_of_progress_bar = "".join(re.findall(r'[0-9]+', progress_bar))
                time.sleep(.7)
                self.driver.execute_script('$("#targetmessage-button-send").click()')
            self.firewalls()
            self.buy_mines()

    def firewalls(self):
        for firewall in range(1, 4):
            to_firewall = f'$("#window-firewall-part{str(firewall)}").click()'
            self.driver.execute_script(to_firewall)
            time.sleep(.4)
            max_charges = self.driver.execute_script('return {}'.format(return_values["max_charges"]))
            max_strength = self.driver.execute_script('return {}'.format(return_values["max_strength"]))
            max_regen = self.driver.execute_script('return {}'.format(return_values["max_regen"]))
            price_max_charges = self.driver.execute_script("return {}".format(return_values["price_max_charges"]))
            price_shop_strength = self.driver.execute_script("return {}".format(return_values["price_shop_strength"]))
            price_shop_regen = self.driver.execute_script("return {}".format(return_values["price_shop_regen"]))
            bit_coins = self.driver.execute_script("return {}".format(return_values["ammount"]))

            if int(max_charges) < firewall_config_charges["max_charges"] and \
                    to_decimal(bit_coins) > to_decimal(price_max_charges):
                self.driver.execute_script("{}".format(clicks["max_charges"]))

            if int(max_strength) < firewall_config_charges["max_strength"] \
                    and to_decimal(bit_coins) > to_decimal(price_shop_strength):
                self.driver.execute_script("{}".format(clicks["shop_strength"]))

            if int(max_regen) < firewall_config_charges["max_regen"] \
                    and to_decimal(bit_coins) > to_decimal(price_shop_regen):

                self.driver.execute_script("{}".format(clicks["shop_regen"]))

            else:
                self.driver.execute_script('$("#window-firewall-pagebutton").click()')
            self.driver.execute_script('$("#window-firewall-pagebutton").click()')  # back button

    def buy_mines(self):
        mine_botnet_price = self.driver.execute_script('return {}'.format(return_values["bot_net"]))
        quantum_price = self.driver.execute_script('return {}'.format(return_values["quantum"]))
        bit_coins = self.driver.execute_script("return {}".format(return_values["ammount"]))

        while to_decimal(bit_coins) > to_decimal(quantum_price):
            self.driver.execute_script('{}'.format(clicks["quantum"]))
            quantum_price = self.driver.execute_script('return {}'.format(return_values["quantum"]))
            bit_coins = self.driver.execute_script("return {}".format(return_values["ammount"]))
            time.sleep(.5)

        while to_decimal(bit_coins) > to_decimal(mine_botnet_price):
            self.driver.execute_script('{}'.format(clicks["botnet"]))
            mine_botnet_price = self.driver.execute_script('return {}'.format(return_values["bot_net"]))
            bit_coins = self.driver.execute_script("return {}".format(return_values["ammount"]))
            time.sleep(.5)


def to_decimal(value):
    return decimal.Decimal(value)


def find_word(link):
    with open("wordlist.txt", "r") as f:
        word = json.loads(f.read())
    return word[link]


if __name__ == '__main__':
    USERNAME = "YOURYOUSERNAME"
    S = SourceIoBot(USERNAME)
    S.login()
    S.attack()
