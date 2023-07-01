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
    # //button[contains(concat(' ',normalize-space(@class),' '),' AccountPanelMenu_target-logout ')]
    try:
        account_menu = WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.XPATH,'//div[@class="logout"]'))
        a.move_to_element(account_menu).perform()
        d.find_element(By.XPATH, '//li[.="Sign Out"]').click()
    except NoSuchElementException:
        pass
    except TimeoutException:
        pass


def login_user(d, a, i):
    
    try:
        print(i)
        login_button = str(os.getenv("LOGINBUTTON"+str(i)))
        print(login_button)
        login_element = d.find_element(By.XPATH,str(login_button))
        WebDriverWait(d, timeout=10).until(lambda d: d.find_element(By.XPATH,login_button))
    except NoSuchElementException:
        print("Cannot find the login ")
        return -1

    login_element.click()

    login_method = os.getenv("LOGIN_METHOD", "UN_PW")
    if login_method == "UN_PW":
        #username and password auth
        try:
            username_input = str(os.getenv("UNINPUT"+str(i)))
            print(username_input)
            username_element = WebDriverWait(d, timeout=10).until(lambda d: d.find_element(By.XPATH,username_input))
        except:
            return -1
        username_element.send_keys(os.getenv("UN"+str(i)))
        password_input = os.getenv("PWINPUT"+str(i))
        d.find_element(By.XPATH,str(password_input)).send_keys(os.getenv("PSWD"+str(i)))
        sign_in_button = os.getenv("SIGNINBUTTON"+str(i))
        d.find_element(By.XPATH, str(sign_in_button)).click()
        after_sign_in_wait = os.getenv("AFTERSIGNIN"+str(i))
    WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH,str(after_sign_in_wait)))
       
    return 0


if __name__ == '__main__':
    #load environment variables
    load_dotenv()


    #initialize webdriver
    #Chrome
    driver = webdriver.Chrome()

    urls = os.getenv("URLS", None)

    if urls == None:
        print("Please supply a URL.")
        exit(1)

    for i, url in enumerate(urls.split(",")):
        print(i)
        wait_element = os.getenv("PAGELOAD"+str(i))
        print(wait_element)
        driver.get(url)
        actions = ActionChains(driver)
        try:
            WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH,str(wait_element)))
        except TimeoutError:
            print("Page did not load.")
            exit(1)
        driver.maximize_window()
        #logout_user(driver, actions)    

        #resp = -1
        #while resp == -1:
        resp = login_user(driver, actions,i)

    #logout_user(driver, actions)    

