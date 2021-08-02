import urllib
import requests
from bs4 import BeautifulSoup, Tag
from collections import Counter
import nltk
from nltk.corpus import stopwords
import unicodedata

words_display = 5

response = requests.get(
    url=input()
)

# print("Code:", response.status_code)

soup = BeautifulSoup(response.content, 'lxml')

title = soup.find(id="firstHeading")
print("Article:", title.text)

sections = soup.select_one(".mw-parser-output").findChildren(recursive=False)

for rmv in sections:

    if rmv.has_attr('id') and (rmv['id'] == 'toc'):
        # print("Removed:",  rmv['id'])
        sections.remove(rmv)
        break


words = dict()

for sect in sections:
    # exits only if start of new sub(section)
    if sect.find(class_="mw-headline"):
        words = dict(
            sorted(words.items(), key=lambda x: x[1], reverse=True))

        print("\t\tCommon Words:", end=" ")
        i = 1
        for value in words:
            if value not in stopwords.words('english'):
                print(value, end=" ")
                i += 1
                if i > words_display:
                    print("")
                    break

        words.clear()

        if sect.text == "References":
            exit()

    # start of (sub)section
    # TEMP
    # if sect.name == "h2":
    #     exit()
    # is a section
    if(sect.find(class_="mw-headline") != None):
        if sect.name == "h2":
            print("Section:", sect.text)
        else:
            print("\tSub-Section:", sect.text)
    else:
        # do word analysis here
        # print(sect.text.encode("UTF8"))
        # print(unicodedata.normalize('NFKC', sect.text))

        # fixes text
        text = sect.text
        text = text.replace('(', '').replace(')', '')
        text = text.split()

        # word analysis
        for word in text:
            word = word.lower()
            if word in words:
                words[word] += 1
            else:
                words.update({word: 1})

        links = sect.find_all('a', {'href': True}, recursive=True)
        if links != None:
            for link in links:
                if link["href"][0] != "#" and link["href"][-11:] != "action=edit":
                    if len(link["href"]) > 5 and "/wiki/" in link["href"][:6].lower():
                        print("\t\t\t\t\tLink: https://en.wikipedia.org" +
                              link["href"])
                    else:
                        print("\t\t\t\t\tLink:", link["href"])
