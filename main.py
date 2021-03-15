from typing import List

from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

def get_currencies(currencies, start, end, export_csv=False):
    frames = []
    print(currencies)
    for currency in currencies:
        print(f'Now trying to get {currency}')
        failCounter = 0
        while True:
            try:

                # Opening the connection and grabbing the page
                my_url = f'https://uk.investing.com/currencies/usd-{currency.lower()}-historical-data'
                option = Options()
                option.headless = False
                driver = webdriver.Chrome(options=option)
                driver.get(my_url)
                driver.maximize_window()


                # Select the date button by its Xpath and then click on it.
                date_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                    "/html/body/div[5]/section/div[8]/div[3]/div/div[2]/span")))

                date_button.click()


                # Sending the start date
                start_bar = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                    "/html/body/div[7]/div[1]/input[1]")))

                start_bar.clear()
                start_bar.send_keys(start)


                # Sending the end date
                end_bar = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                    "/html/body/div[7]/div[1]/input[2]")))

                end_bar.clear()
                end_bar.send_keys(end)


                # Clicking on the apply button
                apply_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                    "/html/body/div[7]/div[5]/a")))

                apply_button.click()
                sleep(5)

                # Getting the tables on the page and quiting
                dataframes = pd.read_html(driver.page_source)
                driver.quit()
                print(f'{currency} scraped.')
                break


            except:
                failCounter += 1
                driver.quit()
                print(f'Failed to scrape {currency}. Trying again in 2 seconds.')
                sleep(2)
                if failCounter == 2:
                    break
                continue

            # Selecting the correct table
                # Selecting the correct table
        for dataframe in dataframes:
            if dataframe.columns.tolist() == ['Date', 'Price', 'Open', 'High', 'Low', 'Change%']:
                df = dataframe
                break
        frames.append(df)

        # Exporting the .csv file
        if export_csv:
            df.to_csv('currency.csv', index=False)
            print(f'{currency}.csv exported.')

    return frames









get_currencies(['jpy'], 2007, 2010, True)