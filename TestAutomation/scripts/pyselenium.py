from selenium import webdriver # pip install selenium
from selenium.webdriver.common.keys import Keys
from PIL import Image, ImageChops
import os, time


def wait_until_load():
	def page_has_loaded(): return driver.execute_script('return document.readyState;') == 'complete'
	time.sleep(1)
	count = 0
	while not(page_has_loaded() or count==10):
		time.sleep(0.25)
		count+=1

def equal_images(im1, im2): return ImageChops.difference(im1, im2).getbbox() is None

testcases = {"testCase1":"x = {-b \pm \sqrt{b^2-4ac} \over 2a}", "testCase2":"x = 5/3", "testCase3":"x = {-b \pm \sqrt{b^5-4acdef} \over 2ba}"}

driver = webdriver.Firefox()
parent_dir_path = "%s/../" %os.path.dirname(os.path.abspath(__file__))
skeleton_file_path = parent_dir_path + "project/src/skeleton.html"
driver.get("file:///" + skeleton_file_path) #navigate to skeleton file
wait_until_load()

for testcase_name in testcases.keys():
	oracle_path = parent_dir_path + "oracles/%s.jpg" % testcase_name
	result_path = parent_dir_path + "temp/testResults/%s.jpg" % testcase_name
	driver.find_element_by_id("MathInput").clear() #clear input box
	driver.find_element_by_id("MathInput").send_keys(testcases[testcase_name]) #type testcase into box
	driver.find_element_by_id("MathInput").send_keys(Keys.RETURN) #hit enter
	wait_until_load()
	# driver.get_screenshot_as_file(oracle_path) #save screenshot (oracle_path to save oracles)
	driver.get_screenshot_as_file(result_path) #save screenshot (result_path to test)
	oracle_image = Image.open(oracle_path)
	result_image = Image.open(result_path)
	equality = equal_images(oracle_image, result_image)
	print testcase_name + ": " + str(equality)
driver.quit()
