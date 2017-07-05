# coding=utf-8
import sys,time
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("..")
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import unittest


class Result(unittest.TestCase):
    def setUp(self):
        self.dr = webdriver.Firefox()
        self.url = "http://www.baidu.com"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_baidu(self):
        self.dr.get(self.url)
        self.dr.find_element_by_id('kw').send_keys('python')
        self.dr.find_element_by_id('su').click()
        print self.dr.title
        time.sleep(3)

    def tearDown(self):
        self.dr.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
