from cgi import print_arguments
from html.parser import HTMLParser
import pandas as pd
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import soupsieve
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# Create URL to scrape,
url = "https://gog-mdat.org/map"
#url = "https://python.org"
#url = "https://google.com"
start = 0
data = []

import warnings
warnings.filterwarnings("ignore")

#def fxn():
#    warnings.warn("deprecated", DeprecationWarning)

#with warnings.catch_warnings():
#    warnings.simplefilter("ignore")
#    fxn()

def highlight(e):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = e._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", e, s)
    original_style = e.get_attribute('style')
    apply_style("background: yellow; border: 10px solid red;")
    time.sleep(.3)
    apply_style(original_style)

while start < 1:
    try:
        # Creeate a request to the URL with the page number
        urlWithPage = url
        browser = webdriver.Chrome('/usr/local/bin/chromedriver')
        browser.maximize_window()
        browser.get(url)
        # Delay is essential to wait for all tiles to be painted
        time.sleep(5)
        browser.find_element_by_xpath("//span[@class='mat-select-min-line ng-tns-c73-4 ng-star-inserted']").click()
        time.sleep(.5)
        # Selects 365 days option
        browser.find_element_by_xpath("//mat-option[@id='mat-option-11']").click()
        time.sleep(.5)
        elements  = browser.find_elements_by_xpath("//*[@id='slider']/ngu-carousel/div/div[1]/div/ngu-tile")
        print("Found " + str(len(elements)) + " tiles")
        for i in range(len(elements)):
            try:
                time.sleep(2)
                print("//*[@id='slider']/ngu-carousel/div/div[1]/div/ngu-tile[" + str(i+1) +"]/div[1]")
                # Tile is sometimes obscured by the map, so we need to click the upper left corder of the tile
                element = browser.find_element_by_xpath("//*[@id='slider']/ngu-carousel/div/div[1]/div/ngu-tile[" + str(i+1) +"]/div[1]")
                action = webdriver.common.action_chains.ActionChains(browser)
                action.move_to_element_with_offset(element, 5, 5)
                action.click()
                action.perform()
                time.sleep(2)
                browser.find_element_by_xpath("//span[normalize-space()='EVENT DETAILS']").click()
 
                row = []      
                xpath = "//*[@id='slider']/ngu-carousel/div/div[1]/div/ngu-tile[" + str(i+1) + "]"
                time.sleep(2)
                try:
                    if (i > 0):
                        browser.find_element_by_xpath("//*[@id='slider']/ngu-carousel/div/button[2]").click()
                except:
                    print("Count not click button to advance to next page")

                # Extract data from tile
                row.append(browser.find_element_by_xpath(xpath + "/div/div/div[1]/span/b").text)
                row.append(browser.find_element_by_xpath(xpath + "/div/div/div[2]/div[1]/div/span[1]/b").text)
                row.append(browser.find_element_by_xpath(xpath + "/div/div/div[2]/div[1]/div/span[2]").text)
                row.append(browser.find_element_by_xpath(xpath + "/div/div/div[2]/div[2]/div/span[1]/b").text)
                row.append(browser.find_element_by_xpath(xpath + "/div/div/div[2]/div[2]/div/span[1]").text)
                row.append(browser.find_element_by_xpath(xpath + "/div/div/div[2]/div[2]/div/span[2]/b").text)
                row.append(browser.find_element_by_xpath(xpath + "/div/div/div[2]/div[2]/div/span[2]").text)
                row.append(browser.find_element_by_xpath(xpath + "/div/div/div[3]/h2/b").text)
                row.append(browser.find_element_by_xpath(xpath + "/div/div/div[3]/h3/span").text)
                row.append(browser.find_element_by_xpath(xpath + "/div/div/div[3]/p").text)
            
                data.append(row)

                try:
                    if (i > 0):
                        browser.find_element_by_xpath("//*[@id='slider']/ngu-carousel/div/div[1]/div/ngu-tile[" + str(i) +"]/div[1]").click()
                except:
                    print("Failed to click forward button at conclusion of loop ")

                time.sleep(2)
            except Exception as e:
                print(i)
                print("Excpetion in clicking element 2")
                print(traceback.format_exc())
    except Exception as e:
        print(e)
        print(traceback.format_exc())

    start = start + 1
                    
browser.close()

if (len(elements) != len(data)):
    print("Carousel had " + str(len(elements)) + " tiles, but we only wrote " + str(len(data)) + " tiles")
else:
    print("Data count matches carousel count")

# Create a dataframe from the data list
df = pd.DataFrame(data)
# Add the column names to the dataframe, could not manually obtain them from HTML accurately
#df.columns = []
# Save the dataframe to a csv file
#df.to_csv('data.csv', header='', index=False)
df.to_csv("data.csv",index=False)
print(df)