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

output_file_path = 'outputs/output_HH_PARSER.json'

pagination = 10  # страниц с обьявлениями
l = 'https://hh.ru/search/resume?page='
l = 'https://penza.hh.ru/search/resume?clusters=true&exp_period=all_time&experience=noExperience&logic=normal&no_magic=false&order_by=relevance&pos=position&skill=3093&skill=1250&text=%EF%F0%EE%E3%F0%E0%EC%EC%E8%F1%F2&area=1&page='



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

	# ОБЩАЯ ИНФА
	try:
		gender = driver.find_element_by_css_selector("span[data-qa='resume-personal-gender']").text  # пол
	except:
		gender = ''

	try:
		age = driver.find_element_by_css_selector("span[data-qa='resume-personal-age']").text        # возраст
	except:
		age = ''

	try:
		birthday = driver.find_element_by_css_selector("span[data-qa='resume-personal-birthday']").text  # др
	except: 
		birthday = ''

	try:
		address = driver.find_element_by_css_selector("span[data-qa='resume-personal-address']").text    # город
	except:
		address = ''


	try:
		relocateRemoval = driver.find_element_by_css_selector("span[data-qa='resume-personal-address']").find_element_by_xpath('..').text.split(',')[-2]  # готов к переезду
	except:
		relocateRemoval = ''


	try:
		relocateComandir = driver.find_element_by_css_selector("span[data-qa='resume-personal-address']").find_element_by_xpath('..').text.split(',')[-1]  # готов к командировкам
	except:
		relocateComandir = ''


	# ВАКАНСИЯ
	try:
		resumeTitlePosition = driver.find_element_by_css_selector("span[data-qa='resume-block-title-position']").text   # название вакансии
	except:
		resumeTitlePosition = ''


	try:
		salary = driver.find_element_by_class_name('resume-block__title-text_salary').text
	except: 
		salary = ''


	try:
		specializationCategory = driver.find_element_by_css_selector("span[data-qa='resume-block-specialization-category']").text  # категория
	except:
		specializationCategory = ''

	try:
		specializations =  [ li.text for li in driver.find_element_by_css_selector("span[data-qa='resume-block-specialization-category']") \
								.find_element_by_xpath('..') \
								.find_element_by_tag_name('ul') \
								.find_elements_by_tag_name('li') ]   # список специализаций
	except:
		specializations = []


	try:
		employment = driver.find_element_by_xpath("//*[contains(text(), 'Занятость:')]").text
	except:
		employment = ''

	try:
		workGraph = driver.find_element_by_xpath("//*[contains(text(), 'График работы:')]").text
	except:
		workGraph = ''

	# ОПЫТ РАБОТЫ

	try:
		experienceTime = driver.find_element_by_class_name('resume-block__title-text_sub').text  
	except:
		experienceTime = ''



	experience = []

	try:
		wordGaps = driver.find_element_by_css_selector("div[data-qa='resume-block-experience']").find_elements_by_class_name('bloko-columns-row')
		for gap in wordGaps[2:]:
			experience.append({
				'dates': gap.find_element_by_tag_name('div').text,  # даты работы
				'titles': [ t.text for t in gap.find_elements_by_class_name('resume-block__sub-title')],   # названия должностей
				'descriptions': [ d.text for d in gap.find_elements_by_css_selector("div[data-qa='resume-block-experience-description']")]  # описания должностей        		                               # даты работы
				})
	except:
		pass

	try:
		skills = [ tag.text for tag in driver.find_element_by_class_name('bloko-tag-list').find_elements_by_css_selector("span[data-qa='bloko-tag__text']") ]   # навыки
	except:
		skills = []


	# дальше общая инфа

	try:
		driving = driver.find_element_by_xpath("//*[contains(text(), 'Права категории')]").find_element_by_xpath('..').text  # права, машина
	except:
		driving = ''



	try:
		about = driver.find_element_by_css_selector("div[data-qa='resume-block-skills-content']").text
	except:
		about = ''


	try:
		educationName = driver.find_element_by_css_selector("div[data-qa='resume-block-education-name']").text 	# название вуза 
	except:
		educationName = ''



	try:
		educationOrg = driver.find_element_by_css_selector("div[data-qa='resume-block-education-organization']").text          # факультет
	except:
		educationOrg = ''


	try:
		languages = [p.text for p in driver.find_elements_by_css_selector("p[data-qa='resume-block-language-item']")]
	except:
		languages = []


	try:
		citizenshipPermissionWay = driver.find_elements_by_xpath("//*[contains(text(), 'Гражданство')]")[1].find_element_by_xpath('..').text  # Гражданство, время в пути до работы
	except:
		citizenshipPermissionWay = ''



	resumeItem = {

		# ОБЩАЯ ИНФА		
		"gender" : gender, 															#	пол								
		"age" : age,																#	возраст
		"birthday" : birthday,														#	др
		"address" : address,														#	адрес	
		"relocateRemoval" : relocateRemoval,										#	переезд		
		"relocateComandir" : relocateComandir,										#	командировка		


		# ЖЕЛАЕМАЯ ДОЛЖНОСТЬ
		"resumeTitlePosition" : resumeTitlePosition,								#	название специализации		
		"salary": salary,															# 	зарплата		
		"specializationCategory" : specializationCategory,							#	категория специализации								
		"specializations" : specializations,										#	массив специализаций							
		"employment" : employment,													#	частичная/полная занятость		
		"workGraph" : workGraph,													#	график работы		


		# ОПЫТ РАБОТЫ
		"experienceTime" : experienceTime,											#	опыт работы				
		"experience" : experience,													#	массив предыдущих работ
		"skills" : skills,															#	ключевые навыки


		# ПРОЧЕЕ
		"driving" : driving,														#	опыт вождения	
		"about" : about,															#	обо мне
		"educationName" : educationName,											#	ВУЗ				
		"educationOrg" : educationOrg,												#	факультет			
		"languages" : languages,													#	массив языков		
		"citizenshipPermissionWay" : citizenshipPermissionWay						#	Гражданство, время в пути до работы									

	}

	# print(resumeItem)
	# print()
	# print()


	# запись
	if(os.path.exists(output_file_path)):	
		with open(output_file_path, "r") as read_file:
			data = json.load(read_file)
			data.append(resumeItem)

			with open(output_file_path, "w") as write_file:
				json.dump(data, write_file)
				write_file.close()
	else:
		with open(output_file_path, "w") as write_file:
			json.dump([resumeItem], write_file)
			write_file.close()



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



	