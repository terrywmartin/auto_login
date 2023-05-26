from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import os
import time

def logout_user(d, a):
    # sign out if the user logged in
    try:
        account_menu = WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.XPATH,'//div[@class="logout"]'))
        a.move_to_element(account_menu).perform()
        d.find_element(By.XPATH, '//li[.="Sign Out"]').click()
    except NoSuchElementException:
        pass
    except TimeoutException:
        pass


def login_user(d, a):
    try:
        login_element = d.find_element(By.XPATH,'//span[.="Login"]')
        WebDriverWait(d, timeout=10).until(lambda d: d.find_element(By.XPATH,'//span[.="Login"]'))
    except NoSuchElementException:
        print("Cannot find the login ")
        return -1

    login_element.click()

    login_method = os.getenv("LOGIN_METHOD", "UN_PW")
    if login_method == "UN_PW":
        #username and password auth
        try:
            username_element = WebDriverWait(d, timeout=10).until(lambda d: d.find_element(By.XPATH,'//form[@class="el-form login-form"]/div[contains(@class,"login-username")]/div/div/div/input'))
        except:
            return -1
        username_element.send_keys(os.getenv("UN"))
        d.find_element(By.XPATH,'//form[@class="el-form login-form"]/div[contains(@class,"login-password")]/div/div/input').send_keys(os.getenv("PSWD"))
        d.find_element(By.XPATH, '//button/span[.="Log in"]/..').click()
        WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH,'//div[@class="logout"]'))
    elif login_method == "GOOGLE":
        try:
            google_login = WebDriverWait(d, timeout=10).until(lambda d: d.find_element(By.XPATH,'//span/img[@src="https://us.olicdn.com/Google.png" ]/..'))
            google_login.click()
            
            ga_email = d.find_element(By.XPATH, '//input[@id="identifierId"]').send_keys(os.getenv("UN"))
            d.find_element(By.XPATH, '//span[.="Next"]/..').click()
            ga_password = WebDriverWait(d, timeout=10).until(lambda d: d.find_element(By.XPATH,'//input[@name="Passwd"]'))
            ga_password.send_keys(os.getenv("GA_PSWD"))
            d.find_element(By.XPATH, '//span[.="Next"]/..').click()

        except NoSuchElementException:
            print("Trouble logging in with Google Auth. ")
            exit(1)

    return 0


if __name__ == '__main__':
    #load environment variables
    load_dotenv()


    #initialize webdriver
    #Chrome
    driver = webdriver.Chrome()

    url = os.getenv("URL", None)

    if url == None:
        print("Please supply a URL.")
        exit(1)

    driver.get(url)
    actions = ActionChains(driver)
    try:
        WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH,'//span[.="Messages"]'))
    except TimeoutError:
        print("Page did not load.")
        exit(1)
    driver.maximize_window()
    logout_user(driver, actions)    

    resp = -1
    while resp == -1:
        resp = login_user(driver, actions)

    logout_user(driver, actions)    

