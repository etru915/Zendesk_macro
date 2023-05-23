# https://coupangcustomersupport.zendesk.com/api/v2/macros.json?page=1&per_page=1000&include=usage_30d,usage_7d

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import uic
from lib.macro_downloader_UI import Ui_MainWindow
from lib.logger import Logger
from lib.macro_request import macro_request
import re
import datetime
import pandas as pd
import json
import urllib3
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller as AutoChrome
import time
import traceback

class Main(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logging = Logger()
        self.plainTextEdit.appendPlainText("****매크로 조회수 다운로더 사용법**** \n -- 1번 버튼을 누르고 로그인을 진행합니다. \n -- 로그인이 완료되면 2번 버튼을 눌러주세요.\n")

        self.locate = os.getcwd()

        self.pushButton_2.clicked.connect(self.pushButton_2_clicked)
        self.pushButton_3.clicked.connect(self.pushButton_3_clicked)
        # 3. EXIT 버튼
        self.pushButton_5.clicked.connect(self.pushButton_5_clicked)

    # 1.Zendesk Log-In 버튼 클릭
    def pushButton_2_clicked(self):
        self.macro = macro_request()
        self.macro.macro_login_setting()
        self.macro.macro_login_page()

        # self.chrome_options = Options()
        # self.logging.log.info("Complete !!")
        # self.chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        # self.logging.log.info("Complete !!")
        # self.driver = webdriver.Chrome(executable_path=self.locate + '\\chromedriver.exe', options=self.chrome_options)
        # self.logging.log.info("Complete !!")
        # self.driver.set_window_size(1500, 900)
        # self.driver.implicitly_wait(15)
        #
        # self.chrome_ver = AutoChrome.get_chrome_version()
        # self.plainTextEdit.appendPlainText("현재 사용중인 크롬 버전은" + self.chrome_ver + " 입니다.")
        # self.plainTextEdit.appendPlainText("현재 사용중인 드라이버 버전은 ChromeDriver 100.0.4896.60 입니다.")
        # self.logging.log.info("Complete !!")
        #
        # self.driver.get('https://coupang.okta.com/app/zendesk/exk8bcxnfe6v9XM3N2p7/sso/saml')
        # self.logging.log.info("Complete !!")
        # self.s = requests.Session()
        # self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
        # self.s.headers.update(self.headers)
        # self.logging.log.info("Complete !!")
        # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # self.logging.log.info("Complete !!")

    # 2. Download Start 버튼 클릭
    def pushButton_3_clicked(self):
        self.macro.macro_api_callout()

        # self.plainTextEdit.appendPlainText("매크로 조회수 다운로더를 실행합니다.\n")
        # self.driver.get('https://coupangcustomersupport.zendesk.com/admin/workspaces/agent-workspace/macros')
        # self.logging.log.info("Complete !!")
        # self.s = requests.Session()
        # self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
        # self.s.headers.update(self.headers)
        # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # self.logging.log.info("Complete !!")
        #
        # for cookie in self.driver.get_cookies():
        #     self.c = {cookie['name']: cookie['value']}
        #     self.s.cookies.update(self.c)
        #     self.logging.log.info("Complete !!")
        #
        # self.i = 1
        # while self.i <= 5:
        #     self.address = 'https://coupangcustomersupport.zendesk.com/api/v2/macros.json?include=usage_30d,usage_7d&page=' + str(self.i)
        #     self.logging.log.info("Complete !!")
        #     self.res = self.s.get(self.address, verify=False)
        #     # self.locate = 'C:\\Users\\zeno915\\Desktop\\macro\\api_raw_new\\macro_list_'
        #     with open(self.locate + "\\" + str(self.i) + '.json', 'w', encoding="utf-8") as f:
        #         f.write(self.res.text)
        #         print(self.res.text)
        #         QtCore.QCoreApplication.processEvents() #아래 메시지 생성이 딜레이 되는 것을 방지
        #         self.plainTextEdit.appendPlainText(str(self.i) + " 번째 요청을 수행하고 응답을 받았습니다.")
        #     self.i += 1

        self.json_total_macro = pd.DataFrame()
        self.list_counter = 1
        while self.list_counter <= 5:
            self.locate = os.getcwd()
            with open(self.locate + "\\" + str(self.list_counter) + ".json", 'r',
                      encoding="utf-8") as json_file:
                self.json_value = json.load(json_file)
                self.logging.log.info("Complete !!")

            # 매크로 기본 정보를 데이터 프레임으로 변환
            self.json_Macros = pd.json_normalize(self.json_value['macros'])
            # Action 정보 값을 DF로 변환
            self.json_actions = pd.json_normalize(self.json_value['macros'], record_path='actions', meta=['id'], errors='ignore')
            # ID열을 시리즈로 만들고 중복 제거
            self.json_actions_drop_dup = self.json_actions['id'].drop_duplicates()
            # 빈 데이터 프레임 df_actions 생성
            self.df_actions = pd.DataFrame()
            self.logging.log.info("Complete !!")

            for self.i in self.json_actions_drop_dup:
                # ID 열의 시리즈 데이터를 i로 순환 시키고, i에 해당하는 필드, 벨류만 가져오기
                self.data = self.json_actions.loc[self.json_actions.id ==  self.i]
                self.data_dict = {}
                # ID를 헤더 개별 id 값을 넣어 열 생성
                self.data_dict['id'] =  self.i
                # 각각의 action 필드와 밸류를 행에서 열로 변환하여 data_dict에 사전 형태로 저장
                for self.j, self.k in zip(self.data['field'], self.data['value']):
                    self.data_dict[self.j] = self.k
                # 저장된 사전을 데이터 프레임으로 변환
                self.data_df = pd.DataFrame([self.data_dict])
                # df_actions에 각 ID별로 정리된 Action 값을 저장
                self.df_actions = pd.concat([self.df_actions, self.data_df], ignore_index=True)
            self.json_page = pd.merge(self.json_Macros, self.df_actions, on='id', how='left')
            self.json_total_macro = pd.concat([self.json_total_macro, self.json_page], ignore_index=True)
            print(f'{self.list_counter} 페이지 작업 완료')
            QtCore.QCoreApplication.processEvents() #아래 메시지 생성이 딜레이 되는 것을 방지
            self.plainTextEdit.appendPlainText(str(self.list_counter) + " 번째 페이지 작업을 완료하였습니다.")
            self.list_counter += 1
            self.json_total_macro.to_excel(self.locate + "\\macro_list_total.xlsx", encoding="EUC-KR")
        QtCore.QCoreApplication.processEvents()  # 아래 메시지 생성이 딜레이 되는 것을 방지
        self.plainTextEdit.appendPlainText("모든 작업을 완료 하였습니다.")
        self.logging.log.info("Complete !!")

    # 3.Exit 버튼 클릭
    def pushButton_5_clicked(self):
        self.driver.quit()
        QtCore.QCoreApplication.quit()

# zeno915@coupang.com
# jjangkyo21!!


if __name__ == "__main__":
    app = QApplication(sys.argv)
    you_view_main = Main()
    you_view_main.show()
    app.exec()
