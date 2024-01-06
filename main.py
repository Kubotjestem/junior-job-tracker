from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import re

data_list = {}

def save_to_list(today, all_offers, junior_offers):
    if today in data_list and len(data_list[today]) >= 2:
        print(f'Two duplicates already exist for {today}. Skipping...')
        return

    data_list.setdefault(today, []).extend([all_offers, junior_offers])

    print(f'Data for {today} was added to the list')

def job_counter(url):
    try:
        driver = webdriver.Chrome()
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'MuiTab-iconWrapper'))
        )

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        jobs_num_element = soup.find('span', {'class': 'MuiTab-iconWrapper'})

        if jobs_num_element:
            number_match = re.search(r'\d+', jobs_num_element.text.strip())

            if number_match:
                number = int(number_match.group())
                return number
            else:
                print("Can't find numbers in text.")
                return None
        else:
            print("Can't find element with number.")
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    finally:
        driver.quit()

# Przykładowe użycie
url_all = 'https://justjoin.it/all-locations/python'
url_junior = 'https://justjoin.it/all-locations/python/experience-level_junior'

result_all = job_counter(url_all)
result_junior = job_counter(url_junior)

if result_all is not None:
    print(f"Number of job offers at {url_all}: {result_all}")
else:
    print(f"I can't find any numbers for {url_all}.")
    
if result_junior is not None:
    print(f"Number of job offers at {url_junior}: {result_junior}")
else:
    print(f"I can't find any numbers for {url_junior}.")

# Zapis do słownika data_list
today = datetime.today().strftime('%Y-%m-%d')
save_to_list(today, result_all, result_junior)

# Wyświetlenie zawartości słownika data_list
print("Contents of data_list:")
for date, offers in data_list.items():
    print(f"{date}: {offers}")


