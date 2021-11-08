from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "C:\Program Files (x86)\chromedriver\chromedriver.exe"
print("ja")
driver = webdriver.Chrome(PATH)
print("ja")


def desmos_functie(a=1,b=2,c=3,d=4):
    driver.get('https://www.desmos.com/calculator?lang=nl')
    time.sleep(3)
    input = str(a) + "x^3" + "+" + str(b) + "x^2" + "+" + str(c) + "x" + "+" + str(a)
    driver.find_element_by_xpath("/html/body").send_keys(input)

desmos_functie()