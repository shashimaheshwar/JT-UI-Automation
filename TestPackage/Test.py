from selenium import webdriver
import time
item="Maaza"
parent="//*[@class='food-details']"
food="/*[@class='header' and contains(text(),'{0}')]".format(item)
inc="//*[@class='increment']"
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)
driver.get("https://www.blacktickets.in/food-select?blockCode=e53abb26-162d-4b3d-a52e-9bc31968cc53")
time.sleep(5)
'''
for elements in driver.find_elements_by_xpath("//*[@class='increment']"):
    for ele in driver.find_elements_by_class_name('header'):
        if ele.text == 'Samosa':
            elements.click()
            time.sleep(2)
            print("Samosa Added")
        else:
            print("No item avaliable")
            time.sleep(2)'''

for ele in driver.find_elements_by_xpath(parent+food):
    if ele.text in 'Maaza,Fanta':
        print(ele.text)
        time.sleep(5)
        driver.find_element_by_xpath(parent+inc).click()
        print("Added item")

time.sleep(5)
driver.close()