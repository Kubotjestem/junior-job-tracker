from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def job_counter(url):
    try:
        #inicalize web
        driver = webdriver.Chrome()

        #open page
        driver.get(url)

        #wait for content to loadd 
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'MuiTab-iconWrapper'))
        )
        #download source code of this page
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        #find element you want to find
        jobs_num_element = soup.find('span', {'class': 'MuiTab-iconWrapper'})

        #check if element was found
        if jobs_num_element:
            number_match = re.search(r'\d+', jobs_num_element.text.strip())
            
            if number_match:
                number = int(number_match.group())
                return number
            else:
                print("Nie można znaleźć cyfr w tekście.")
                return None
        else:
            print("Nie można znaleźć elementu z liczbą.")
            return None
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return None
    finally:
        #cloce webpage
        driver.quit()


url = 'https://justjoin.it/all-locations/python'
result = job_counter(url)

if result is not None:
    print(f"Number of job offers is {url}: {result}")
else:
    print("I can't find any numbers sorry :(")
