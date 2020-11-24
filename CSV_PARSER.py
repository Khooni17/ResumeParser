# pip install beautifulsoup4 selenium lxml 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import os
import csv

output_file_path = 'outputs/output_CSV_PARSER.csv'


pagination = 1  # страниц с обьявлениями
l = 'https://hh.ru/search/resume?page='



try:
	path = os.path.join(os.path.abspath(os.path.dirname(__file__)), output_file_path)
	os.remove(path)
except:
	pass



### настройка
ua = dict(DesiredCapabilities.CHROME)
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x935')
driver = webdriver.Chrome(options=options, executable_path='driver/chromedriver.exe')
###


def parseResume(l):
	driver.get(l)


	# ВАКАНСИЯ
	try:
		resumeTitlePosition = driver.find_element_by_css_selector("span[data-qa='resume-block-title-position']").text.encode("utf-8").decode("utf-8")  # название вакансии
	except:
		resumeTitlePosition = ''


	try:
		about = driver.find_element_by_css_selector("div[data-qa='resume-block-skills-content']").text.encode("utf-8").decode("utf-8")
	except:
		about = ''


	fields=[about,resumeTitlePosition]
	with open(output_file_path, 'a', encoding="utf-8") as f:
		writer = csv.writer(f, delimiter=';')
		writer.writerow(fields)



linksResume = []
print('получение списка..')
for p in range(pagination):
	print('страница ' + str(p))
	driver.get(l+str(p))

	body = driver.find_element_by_tag_name("body");
	items = body.find_elements_by_class_name("resume-search-item__name");

	for item in items:
		linksResume.append(item.get_attribute("href"))


for i,l in enumerate(linksResume):
	print(str(i)+'/'+str(len(linksResume)))
	parseResume(l)


print('готово')

# l = 'https://hh.ru/resume/4fea78920008356d8b0039ed1f497951747264?hhtmFrom=resume_search_result'
# l = 'https://hh.ru/resume/489598f90005efc0950039ed1f506c46576564?hhtmFrom=resume_search_result'



	