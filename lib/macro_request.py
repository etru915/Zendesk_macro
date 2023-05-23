import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import uic
from lib.logger import Logger
import re
import datetime
import pandas as pd
from lib.macro_downloader_UI import Ui_MainWindow
import json
import urllib3
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller as AutoChrome

class macro_request():
    def __init__(self):
        self.locate = os.getcwd()
        self.messege = "체크체크"

    def macro_login_setting(self):
        self.chrome_options = Options()
        self.chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        self.driver = webdriver.Chrome(executable_path=self.locate + '\\chromedriver.exe', options=self.chrome_options)
        self.driver.set_window_size(1500, 900)
        self.driver.implicitly_wait(15)
        self.chrome_ver = AutoChrome.get_chrome_version()
        # self.plainTextEdit.appendPlainText("현재 사용중인 크롬 버전은" + self.chrome_ver + " 입니다.")
        # self.plainTextEdit.appendPlainText("현재 사용중인 드라이버 버전은 ChromeDriver 100.0.4896.60 입니다.")
        # self.logging.log.info("Complete !!")

    def macro_login_page(self):
        self.driver.get('https://coupang.okta.com/app/zendesk/exk8bcxnfe6v9XM3N2p7/sso/saml')
        self.s = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
        self.s.headers.update(self.headers)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def macro_api_callout(self):
        self.driver.get('https://coupangcustomersupport.zendesk.com/admin/workspaces/agent-workspace/macros')
        self.s = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
        self.s.headers.update(self.headers)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        for cookie in self.driver.get_cookies():
            self.c = {cookie['name']: cookie['value']}
            self.s.cookies.update(self.c)

        self.i = 1
        while self.i <= 40:
            self.address = 'https://coupangcustomersupport.zendesk.com/api/v2/macros.json?&per_page=100&include=usage_1h,usage_24h,usage_7,usage_30d&page=' + str(self.i)
            self.res = self.s.get(self.address, verify=False)
            with open(self.locate + "\\" + str(self.i) + '.json', 'w', encoding="utf-8") as f:
                f.write(self.res.text)
                print(self.res.text)
                QtCore.QCoreApplication.processEvents()  # 아래 메시지 생성이 딜레이 되는 것을 방지
            self.json_value = json.loads(self.res.text)
            print(str(self.i*1000) + "건 저장 완료! -----  총 " + str(self.json_value['count']) + "건")
            if self.json_value['next_page'] is None:
                break
            self.i += 1


if __name__ == '__main__':
    macro_callout = macro_request()
    wait = input("응답대기")
    macro_callout.macro_login_setting()
    macro_callout.macro_login_page()
    wait = input("응답대기")
    macro_callout.macro_api_callout()