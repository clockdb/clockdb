
from φ.models import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe')

for entity in Entity:

    driver.get('http://127.0.0.1:8000/INTC/')

    #link = driver.find_element_by_name("Opinion")

    #link.click()

    try:
        link = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "Opinion"))
        )
        link.click()
        #
    except:
        pass

    ValuationRatio = driver.find_element_by_id("Clockφ1").text

    print(ValuationRatio)

    driver.quit()


