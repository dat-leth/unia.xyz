import requests
from bs4 import BeautifulSoup

# Getting the website
url = "https://www.uni-augsburg.de/de/fakultaet/fai/informatik/studium/lehre/bsc-inf2018/"
response = requests.get(url)

# Extracting the links
soup = BeautifulSoup(response.text, 'html.parser')
courses = soup.find('div', class_="textEditorContent").findAll('a')
results = {}
for course in courses:
    results[course.find('b').string] = course.get('href')
print(results)
