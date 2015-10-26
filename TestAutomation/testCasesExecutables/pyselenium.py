from selenium import webdriver
import os

driver = webdriver.Firefox()
filePath = "file:///%s/test.html" %os.path.dirname(os.path.abspath(__file__))
driver.get(filePath) #skeleton file goes here

# driver.find_element_by_id('search_form_input_homepage').send_keys("realpython")
# driver.find_element_by_id("search_button_homepage").click()
driver.quit()


# IMAGE COMPARISON
# import ImageChops
# def equal(im1, im2):
#     return ImageChops.difference(im1, im2).getbbox() is None