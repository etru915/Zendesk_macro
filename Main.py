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


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.locate = os.getcwd()
        self.logging = Logger()

        self.plainTextEdit.appendPlainText("****매크로 조회수 다운로더 사용법**** \n    1번 버튼을 누르고 로그인을 진행합니다. \n    로그인이 완료되면 2번 버튼을 눌러주세요.\n")


        # 라디오 버튼 기본값 설정
        self.radioButton_2.setChecked(True)
        self.radioButton_3.setChecked(True)
        self.radioButton_10.setChecked(True)
        self.radioButton_5.setChecked(True)

        # 1.Zendesk Log-In 버튼 클릭
        self.pushButton_2.clicked.connect(self.pushButton_2_clicked)
        # 2. Download Start 버튼 클릭
        self.pushButton_3.clicked.connect(self.pushButton_3_clicked)
        # 3. EXIT 버튼
        self.pushButton_5.clicked.connect(self.pushButton_5_clicked)
        # 현재 주소 표시, 폴더 지정 시 내용 변경
        self.lineEdit.setText(str(self.locate))
        self.toolButton.clicked.connect(self.toolButton_clicked)
        self.plainTextEdit.appendPlainText("파일 저장 위치 : " + self.lineEdit.displayText())
        self.folder_name = self.lineEdit.displayText()


    def filter_action(self):
        # active Filter
        if self.radioButton_2.isChecked():
            self.active_filter = "&active=true"
        else:
            self.active_filter = ""

        # Category Filter
        if self.radioButton_4.isChecked():
            self.category_filter = "&categoty=cs|km"
        else:
            self.category_filter = ""

        # Sort_order
        if self.radioButton_9.isChecked():
            self.sort_order = "&sort_order=desc"
        else:
            self.sort_order = ""

        # Sort_by
        if self.radioButton_6.isChecked():
            self.sort_by = "&sort_by=created_at"
        elif self.radioButton_11.isChecked():
            self.sort_by = "&sort_by=updated_at"
        elif self.radioButton_12.isChecked():
            self.sort_by = "&sort_by=usage_24h"
        elif self.radioButton_13.isChecked():
            self.sort_by = "&sort_by=usage_7d"
        elif self.radioButton_14.isChecked():
            self.sort_by = "&sort_by=usage_30d"
        else:
            self.sort_by = ""

        return self.active_filter + self.category_filter + self.sort_order + self.sort_by

    # 1.Zendesk Log-In 버튼 클릭
    def pushButton_2_clicked(self):
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.logging.log.info("Complete !!")
        self.chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        self.logging.log.info("Complete !!")
        self.driver = webdriver.Chrome(executable_path=self.locate + '\\chromedriver.exe', options=self.chrome_options)
        self.logging.log.info("Complete !!")
        self.driver.set_window_size(1500, 900)
        self.driver.implicitly_wait(15)

        self.chrome_ver = AutoChrome.get_chrome_version()
        self.plainTextEdit.appendPlainText("현재 사용중인 크롬 버전은" + self.chrome_ver + " 입니다.")
        self.plainTextEdit.appendPlainText("현재 사용중인 드라이버 버전은 ChromeDriver 100.0.4896.60 입니다.")
        self.logging.log.info("Complete !!")

        self.driver.get('https://coupang.okta.com/app/zendesk/exk8bcxnfe6v9XM3N2p7/sso/saml')
        self.logging.log.info("Complete !!")
        self.s = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
        self.s.headers.update(self.headers)
        self.logging.log.info("Complete !!")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.logging.log.info("Complete !!")

    # 2. Download Start 버튼 클릭
    def pushButton_3_clicked(self):
        self.plainTextEdit.appendPlainText("매크로 조회수 다운로더를 실행합니다.\n")
        self.driver.get('https://coupangcustomersupport.zendesk.com/admin/workspaces/agent-workspace/macros')
        self.logging.log.info("Complete !!")
        self.s = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
        self.s.headers.update(self.headers)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.logging.log.info("Complete !!")

        for cookie in self.driver.get_cookies():
            self.c = {cookie['name']: cookie['value']}
            self.s.cookies.update(self.c)
            self.logging.log.info("Complete !!")

        self.file_list = []
        self.i = 1
        while self.i <= 40:
            # API Requests 주소 생성부
            self.address = 'https://coupangcustomersupport.zendesk.com/api/v2/macros.json?page=' + str(self.i) + "&per_page=1000"
            self.address_include = "&include=usage_1h,usage_24h,usage_7d,usage_30d"
            self.address_filter = self.filter_action()
            self.full_address = self.address + self.address_include + self.address_filter
            print(self.full_address)
            self.logging.log.info("Complete !!")

            # API Requests 요청 시작
            self.res = self.s.get(self.full_address, verify=False)
            self.logging.log.info("self.res Complete !!")
            QtCore.QCoreApplication.processEvents()  # 아래 메시지 생성이 딜레이 되는 것을 방지
            self.plainTextEdit.appendPlainText(str(self.i) + " 번째 요청을 수행하고 응답을 받았습니다.")
            # self.locate = 'C:\\Users\\zeno915\\Desktop\\macro\\api_raw_new\\macro_list_'

            # API Requests 응답 내용을 Json 파일로 저장
            self.cur_time = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
            with open(self.folder_name + "\\" + str(self.i)+"__" + self.cur_time + '.json', 'w', encoding="utf-8") as f:
                f.write(self.res.text)
                print(self.res.text)
                self.file_list.append(str(self.i)+"__" + self.cur_time + '.json')
            self.json_value = json.loads(self.res.text)
            QtCore.QCoreApplication.processEvents() #아래 메시지 생성이 딜레이 되는 것을 방지
            self.plainTextEdit.appendPlainText(str(self.i * 1000) + "건 저장 완료! -----  총 " + str(self.json_value['count']) + "건")

            if self.json_value['next_page'] is None:
                break
            self.i += 1

        self.json_total_macro = pd.DataFrame()
        self.list_counter = 1
        print(self.file_list)

        for i in self.file_list:
            with open(self.folder_name + "\\" + i, 'r', encoding="utf-8") as json_file:
                self.json_value = json.load(json_file)
                self.logging.log.info("Complete !!")

        # while self.list_counter <= 5:
            # self.locate = os.getcwd()
            # with open(self.locate + "\\" + str(self.list_counter) + ".json", 'r',
            #           encoding="utf-8") as json_file:
            #     self.json_value = json.load(json_file)
            #     self.logging.log.info("Complete !!")

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
        self.cur_time = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        self.json_total_macro.to_excel(self.folder_name + "\\macro_list_total"+ self.cur_time +".xlsx", encoding="EUC-KR")
        QtCore.QCoreApplication.processEvents()  # 아래 메시지 생성이 딜레이 되는 것을 방지
        self.plainTextEdit.appendPlainText("모든 작업을 완료 하였습니다.")
        self.logging.log.info("Complete !!")

    # 3.Exit 버튼 클릭
    def pushButton_5_clicked(self):
        self.driver.quit()
        QtCore.QCoreApplication.quit()

    def toolButton_clicked(self):
        global folder_locate
        self.folder_locate = QFileDialog.getExistingDirectory(self,'Open File')
        self.lineEdit.setText(str(self.folder_locate))
        self.folder_name = self.lineEdit.displayText()
        self.plainTextEdit.appendPlainText("변경된 파일 저장 위치 : " + self.lineEdit.displayText())



# zeno915@coupang.com
# jjangkyo21!!


if __name__ == "__main__":
    app = QApplication(sys.argv)
    you_view_main = Main()
    you_view_main.show()
    app.exec()
