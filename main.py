import sys
import time
import pyperclip
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class NaverLoginService():

    id = ""
    pw = ""

    def __init__(self, id, pw):
        self.driver = None
        self.id = id
        self.pw = pw

    def open_web_mode(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.implicitly_wait(120)

    def get_driver(self):
        return self.driver

    def close_browser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def login(self):
        self.driver.get("https://nid.naver.com/nidlogin.login")
        time.sleep(2)  # 페이지 로딩 대기

        # 아이디 입력
        id_input = self.driver.find_element(By.ID, "id")
        id_input.click()
        pyperclip.copy(self.id)
        actions = ActionChains(self.driver)
        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        time.sleep(1)  # 입력 후 잠시 대기

        # 패스워드 입력
        pw_input = self.driver.find_element(By.ID, "pw")
        pw_input.click()
        pyperclip.copy(self.pw)
        actions = ActionChains(self.driver)
        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        time.sleep(1)  # 입력 후 잠시 대기

        # 로그인 버튼 클릭
        self.driver.find_element(By.ID, "log.login").click()

    def run(self):
        self.open_web_mode()
        self.login()
        return self.driver

class NaverIDExtractor():
    driver = None

    def __init__(self, driver):
        self.driver = driver

    def get_id(self):
        idList = []
        authors = list(self.driver.find_elements(By.CLASS_NAME, "author"))
        for author in authors:
            idList.append(
                str(author.get_attribute('href')).split("/")[len(str(author.get_attribute('href')).split("/")) - 1]
            )

        return idList

    def saveAllId(self, idList):
        f = open('idList.txt', 'a')
        r = open('idList.txt', 'r')
        for id in idList:
            if not id in r.readlines():
                f.write(id + "\n")
        f.close()
        r.close()

    def getAllId(self, pageCount):
        self.driver.get("https://section.blog.naver.com/BlogHome.naver?directoryNo=0&currentPage=1&groupId=0")
        time.sleep(2)

        idList = []
        print("아이디 추출중 . . .")

        for page in range(1, pageCount + 1):
            idList += self.get_id()
            self.driver.get(f"https://section.blog.naver.com/BlogHome.naver?directoryNo=0&currentPage={page}&groupId=0")

        self.saveAllId(idList=idList)

        return idList

if __name__ == "__main__":
    try:
        pageCount = int(input("가져올 페이지 개수 : "))
        if pageCount <= 0:
            print("옳지 않은 입력!")
            sys.exit()
    except Exception:
        print("옳지 않은 입력!")
        sys.exit()

    userId = input("아이디 : ")
    userPw = input("비밀번호 : ")

    naver_service = NaverLoginService(userId, userPw)
    driver = naver_service.run()

    naver_id = NaverIDExtractor(driver=driver)
    idList = naver_id.getAllId(pageCount=pageCount)

    for id in idList:
        print("찾은 아이디 : " + str(id))

    driver.quit()
    sys.exit()
