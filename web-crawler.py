# -*- coding: utf-8 -*-
"""webcrawler.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p8CaHwkQX4kIB-DrumlvUQXcHm9XyqTS
"""

!pip install selenium
!apt-get update # to update ubuntu to correctly run apt install
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin

#Create 101 directories in google share drive
import pandas as pd
import os
os.chdir('final_project')
#read the name classes file
column_names=["index","name"]
df = pd.read_csv("tw_food_101_classes.csv", names=column_names)
foods = df.name.to_list()
#create directories
for food_name in foods:
  if os.path.isdir(food_name):
    break
  else:
    os.mkdir(food_name)

chinese_food_name = []
name = ''
with open("101_food_name.txt") as fh:
    for line in fh.readlines():
      for word in line:
        if word != '\n':
          name += word
        else:
          chinese_food_name.append(name)   
          name = ''

import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver

# Creating a webdriver instance
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('chromedriver',options=chrome_options)

# Maximize the screen
driver.maximize_window()

# Function for scrolling to the bottom of Google
# Images results
def scroll_to_bottom():

    last_height = driver.execute_script('\
    return document.body.scrollHeight')

    while True:
        driver.execute_script('\
        window.scrollTo(0,document.body.scrollHeight)')

        # waiting for the results to load
        # Increase the sleep time if your internet is slow
        time.sleep(3)

        new_height = driver.execute_script('\
        return document.body.scrollHeight')

        # click on "Show more results" (if exists)
        try:
            driver.find_element(by='xpath', value=".YstHxe input").click()

            # waiting for the results to load
            # Increase the sleep time if your internet is slow
            time.sleep(3)

        except:
            pass

        # checking if we have reached the bottom of the page
        if new_height == last_height:
            break

        last_height = new_height

def web_crawler(num):

  # Open Google Images in the browser
  driver.get('https://images.google.com/')

  # Finding the search box
  box = driver.find_element(by='xpath', value='//*[@id="sbtc"]/div/div[2]/input')

  # What you enter here will be searched for in Google Images
  query = chinese_food_name[num]

  # Type the search query in the search box
  box.send_keys(query)

  # Pressing enter
  box.send_keys(Keys.ENTER)

  # NOTE: If you only want to capture a few images,
  # there is no need to use the scroll_to_bottom() function.
  scroll_to_bottom()

  # Loop to capture and save each image
  for i in range(1,400):

    # range(1, 50) will capture images 1 to 49 of the search results
    # You can change the range as per your need.
    try:

      # XPath of each image
        #img = driver.find_element_by_xpath(
            #'//*[@id="islrg"]/div[1]/div[' +
          #str(i) + ']/a[1]/div[1]/img')'''
        img = driver.find_element(by='xpath', value= 
            '//*[@id="islrg"]/div[1]/div['
            + str(i) +
            ']/a[1]/div[1]/img')

        # Enter the location of folder in which
        # the images will be saved
        img.screenshot('final_project/' +
                       '/' 
                       + foods[num] +
                       '/'
                       +
                       ' (' + str(i) + ').png')
        # Each new screenshot will automatically
        # have its name updated

        # Just to avoid unwanted errors
        time.sleep(0.2)

    except:

        # if we can't find the XPath of an image,
        # we skip to the next image
        continue

for i in range(0,101):
  web_crawler(i)

driver.close()