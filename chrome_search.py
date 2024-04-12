from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Setup Chrome options to run headless and disable GPU
chrome_options = Options()

# Set the path to the chromedriver and initialize it using Service
service = Service(
    executable_path="C:\\Users\\s_chohy121212\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
)
driver = webdriver.Chrome(service=service, options=chrome_options)


def search_google_maps(english_name):
    driver.get("https://www.google.co.kr/maps/?hl=ko")
    time.sleep(2)
    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.clear()
    search_box.send_keys(english_name)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)
    try:
        # h1 내부의 span 중 클래스가 'aSH0ec'인 첫 번째 요소의 텍스트를 가져옵니다.
        korean_name_element = driver.find_element(By.CSS_SELECTOR, "h1.aSH0ec")
        korean_name = korean_name_element.text
    except Exception as e:
        korean_name = "Not found"
    return korean_name


# Example usage
english_names_sample = ["Chwimala"]
korean_names_mapping = {name: search_google_maps(name) for name in english_names_sample}

driver.quit()

print(korean_names_mapping)
