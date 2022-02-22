import time
import requests
import shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open("characters.txt","r") as f:
    text = f.read()

batch_amount = 20

for usr_input in range(0, len(text) ,batch_amount):
    driver = webdriver.Firefox()
    URL = "https://www.chineseconverter.com/en/convert/chinese-stroke-order-tool"
    driver.get(URL)

    inputElement = driver.find_element(By.ID, "strokeorder-input")
    inputElement.send_keys(text[usr_input:usr_input+batch_amount])
    
    # select = driver.find_element(By.ID, "bg-color-div")
    # driver.execute_script("arguments[0].style = arguments[1]", select, "background: rgb(0, 0, 0) none repeat scroll 0% 0%;")

    # select = driver.find_element(By.ID, "stroke-color-div")
    # driver.execute_script("arguments[0].style = arguments[1]", select, "background: rgb(255, 255, 255) none repeat scroll 0% 0%;")

    select = Select(driver.find_element(By.ID, 'strokeorder-speedtype'))

    # select by value 
    select.select_by_value('fast') 

    while (True):
        try:
            driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary.btn-lg.btn-extra-large").click()
            break;
        except Exception as e:
            print("EXCEPTON: " + str(e));
            time.sleep(1)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".stroke_order")))

    time.sleep(1)

    src_arr = []

    for character in range(len(text[usr_input:usr_input+batch_amount])):
        img = driver.find_element(By.ID, "stroke_order_" + str(character))
        src = img.get_attribute("src")
        src_arr.append(src)

    for character, count in zip(text[usr_input:usr_input+batch_amount], range(len(text[usr_input:usr_input+batch_amount]))):
        try:
            r = requests.get(src_arr[count], stream=True)
        except Exception as e:
            print(e)
        if r.status_code == 200:
            with open(character + '.gif', 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
    driver.quit()
