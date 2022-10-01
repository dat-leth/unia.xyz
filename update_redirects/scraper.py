import requests
import toml
from bs4 import BeautifulSoup

# Getting the website
url = "https://www.uni-augsburg.de/de/fakultaet/fai/informatik/studium/lehre/bsc-inf2018/"
response = requests.get(url)

# Extracting the links
soup = BeautifulSoup(response.text, 'html.parser')
courses = soup.find('div', class_="textEditorContent").findAll('a')
uni_links = {}
for course in courses:
    uni_links[course.find('b').string.strip()] = course.get('href')


# Open Toml file for redirects
with open('./redirects.toml', 'r', encoding='utf-8') as file:
    redirects = toml.loads(file.read())

uni_key_from = {
    "Informatik 1": ["Informatik 1"],
    "Programmierkurs": ["Java-Programmierkurs", "C-Programmierkurs", "Programmierkurs in C"],
    "Mathematik für Informatik I": ["Mathematik für Informatiker I"],
    "Diskrete Strukturen und Logik": ["Diskrete Strukturen und Logik (beinhaltet Diskrete Strukturen für Informatiker)"],
    "Lineare Algebra I": ["Lineare Algebra I"],
    "Informatik 2": ["Informatik 2"],
    "Mathematik für Informatik II": ["Mathematik für Informatiker II"],
    "Einführung in die Theoretische Informatik": ["Einführung in die Theoretische Informatik"],
    "Analysis I": ["Analysis 1"],
    "Informatik 3": ["Informatik III", 'Informatik 3'],
    "Stochastik für Informatiker": ["Stochastik für Informatiker"],
    "Datenbanksysteme": ["Datenbanksysteme I"],
    "Systemnahe Informatik": ["Systemnahe Informatik"],
    "Softwareprojekt": ["Softwareprojekt"],
    "Grundlagen der Human-Computer-Interaction / Multimedia Grundlagen II":
        ["Grundlagen der Human-Computer Interaction / Multimedia Grundlagen II"],
    "Kommunikationssysteme": ["Kommunikationssysteme"],
    "Grundlagen der Signalverarbeitung und des maschinellen Lernens / Multimedia Grundlagen I": ["Grundlagen der Signalverarbeitung und des Maschinellen Lernens (Multimedia Grundlagen I)"],
    "Softwaretechnik": ["Softwaretechnik"],

}

# Modify Toml representation
for section in redirects["section"]:
    if "link" in section:
        for our_link in section["link"]:                            # Iterate all the redirects
            if our_link["desc"] in uni_key_from:                    # Is our redirect one that can be updated?
                for uni_link in uni_key_from[our_link["desc"]]:     # Iterate all possible Names the uni will give it
                    if uni_link in uni_links:                       # Was it found on the Website as that name?
                        our_link["target"] = uni_links[uni_link]    # Update the link we use
                        print(our_link["desc"] + " <- " + uni_link) # Display the updated links for diagnostic purposes

# Safe Toml file
with open('./redirects.toml', 'w', encoding='utf-8') as file:
    file.write(toml.dumps(redirects))

