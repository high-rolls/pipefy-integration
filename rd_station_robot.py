from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import re
import time


def upload_deal_files(deal, files=None):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    #driver.implicitly_wait(10) # usar espera implicita em todos os comandos
    driver.get(f"https://plugcrm.net/app#/deals/{deal}")
    
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys("dev@seguralta.com.br")
    
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("EDcP9Mrt2RxnAQ")
    
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
    submit_button.click()

    link_instancia = wait.until(lambda d: d.find_element(By.LINK_TEXT, "Seguralta Corretora de Seguros"))
    link_instancia.click()
    
    close_dialog_button = driver.find_element(By.CSS_SELECTOR, "body > div.plug-crm-app > div.md-dialog-container > md-dialog > div > button")
    if close_dialog_button:
        close_dialog_button.click()
    
    aba_arquivos = driver.find_element(By.CSS_SELECTOR, "md-tab-item:nth-child(6)")
    aba_arquivos.click()
    
    file_upload_input = driver.find_element(By.CSS_SELECTOR, "#upload-file-input > input[type=file]")
    files_string = "\n".join(files)
    file_upload_input.send_keys(files_string)

    file_table = driver.find_element(By.CSS_SELECTOR, "#deal_container > div > div.layout-padding.flex > div:nth-child(2) > md-card > md-table-container > table")
    wait.until(lambda d: "Uploading..." not in file_table.text)
    driver.close()

if __name__ == "__main__":
    upload_deal_files("6254368e507374000f9fac61", [
        "C:/Users/paulo.pivotto/Documents/Python/pipefy-integration/rd_station_robot.py",
        "C:/Users/paulo.pivotto/Pictures/Robots-Square-300x300.jpg"])
    print("end of test")