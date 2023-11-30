import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import lxml
import csv
from itertools import zip_longest
import time

# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)

titles = []
company = []
loc = []
skills = []
links = []
salary = []

result = requests.get(f'https://wuzzuf.net/search/jobs/?a=spbg&q=python')
src = result.text
soup = BeautifulSoup(src, 'lxml')

# Job title, Job skills, Company name, Location
job_title = soup.find_all('h2', {'class':'css-m604qf'})
company_name = soup.find_all('a', {'class':'css-17s97q8'})
locations = soup.find_all('span', {'class':'css-5wys0k'})
job_skills = soup.find_all('div', {'class':'css-y4udm8'})

for i in range(len(job_title)):
    titles.append(job_title[i].text)
    company.append(company_name[i].text)
    loc.append(locations[i].text)
    skills.append(job_skills[i].text)
    links.append(job_title[i].find('a').attrs['href'])

prefix = 'https://wuzzuf.net'
links = [prefix + item for item in links]

# for l in links:
#     driver.get(l)
#     # time.sleep(5)
#     src = driver.page_source
#     soup = BeautifulSoup(src, 'html.parser')
#     sal = soup.find_all('span', {'class':'css-4xky9y'})[3]
#     salary.append(sal.text)
#     print(salary)

for l in links:
    result = requests.get(l)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    span = soup.find('h1', {'span' : 'css-47jx3m'})
    sal = span.find('span', class_='css-4xky9y').get_text()
    print(l)
    print(soup)
    break

file_list = [titles, company, loc, skills, links, salary]
exported = zip_longest(*file_list)
#
with open('Scrape.csv', 'w', newline='') as file:
    wr = csv.writer(file)
    wr.writerow(['Job Title', 'Company Name', 'Location', 'Job Skills', 'Link', 'Salary'])
    wr.writerows(exported)