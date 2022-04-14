from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import os


def upload_deal_files(deal, files=None):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    #driver.implicitly_wait(10) # usar espera implicita em todos os comandos
    driver.get(f"https://plugcrm.net/app#/deals/{deal}")

    # login page
    driver.find_element(By.ID, "email").send_keys("dev@seguralta.com.br")
    driver.find_element(By.ID, "password").send_keys("EDcP9Mrt2RxnAQ")
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

    wait.until(lambda d: d.find_element(By.LINK_TEXT, "Seguralta Corretora de Seguros")).click()
    
    dialog_close_button_By = (By.CSS_SELECTOR, "md-dialog .dialog-header button")
    if driver.find_elements(*dialog_close_button_By):
        driver.find_element(*dialog_close_button_By).click()
    
    time.sleep(1)
    aba_arquivos = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "md-tab-item:nth-child(6)")))
    aba_arquivos.click()
    
    driver.find_element(By.CSS_SELECTOR, "#upload-file-input > input[type=file]").send_keys("\n".join(files))
    wait.until(lambda d: "Uploading..." not in driver.find_element(By.CSS_SELECTOR, "#deal_container table").text)

    driver.close()


def create_opportunity():
    api_token = os.getenv("RD_STATION_API_TOKEN")


if __name__ == "__main__":
    upload_deal_files("6254368e507374000f9fac61", [
        "C:/Users/paulo.pivotto/Documents/Python/pipefy-integration/rd_station_robot.py",
        "C:/Users/paulo.pivotto/Pictures/Robots-Square-300x300.jpg"])
    print("end of test")