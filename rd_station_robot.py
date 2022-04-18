from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re
import requests
import time
import os


def upload_deal_files(deal, files=None):
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
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
    
    time.sleep(10)

    driver.find_element(By.CSS_SELECTOR, "md-tab-item:nth-child(6)").click()
    # aba_arquivos = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "md-tab-item:nth-child(6)")))
    # aba_arquivos.click()
    
    driver.find_element(By.CSS_SELECTOR, "#upload-file-input > input[type=file]").send_keys("\n".join(files))
    wait.until(lambda d: "Uploading..." not in driver.find_element(By.CSS_SELECTOR, "#deal_container table").text)

    driver.close()


def create_opportunity(name, email=None):
    api_token = os.getenv("RD_STATION_API_TOKEN")
    user_id = os.getenv("RD_STATION_USER_ID")
    deal_stage_id = os.getenv("RD_STATION_DEAL_STAGE_ID")
    if not api_token or not user_id or not deal_stage_id:
        print("Please set the environment variables RD_STATION_API_TOKEN, RD_STATION_USER_ID, RD_STATION_DEAL_STAGE_ID")
        return
    url = f"https://plugcrm.net/api/v1/deals?token={api_token}"
    data = {
        'deal': {
            'name': name,
            'user_id': user_id,
            'deal_stage_id': deal_stage_id
        },
        'contacts': [
            {
                'name': name,
                'emails': [
                    {
                        'email': email
                    }
                ],
                'phones': [
                    {
                        'phone': '1199999999'
                    }
                ]
            }
        ],
        'organization': {
            'name': name
        }
    }
    res = requests.post(url, json=data)
    res.raise_for_status()
    res_obj = json.loads(res.text)
    return res_obj["id"]


if __name__ == "__main__":
    upload_deal_files("6254368e507374000f9fac61", [
        "C:/Users/high/Documents/git/pipefy-integration/rd_station_robot.py",
        "C:/Users/high/Documents/GD/stc3D/fonts/Montserrat-Medium.ttf"])
    print("end of test")