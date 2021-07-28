import urllib
import requests
from bs4 import BeautifulSoup, Tag
from collections import Counter
import nltk
from nltk.corpus import stopwords

response = requests.get(
    url="https://en.wikipedia.org/wiki/cat"
)

print("Code:", response.status_code)

soup = BeautifulSoup(response.content, 'lxml')

title = soup.find(id="firstHeading")
print("Article:", title.text)

# cltur k c/u
headers = soup.select(".mw-headline")


for sc in headers:

    if sc.parent.name == "h2":
        print("\tSection:", sc.text)
    elif sc.text == "References" or sc.text == "Reference":
        quit()
    else:
        print("\t\tSub-Section:", sc.text)
    sc = sc.parent
    sc = sc.find_next_sibling()

    wordOcur = dict()
    while sc != None and sc.find(class_="mw-headline") == None:
        if len(sc.text) > 0:
            # print("\t\t\t\tText:", sc.text)
            # do word analysis

            text = sc.text
            text = text.split()

            for w in text:
                w = w.lower()
                if w in wordOcur:
                    wordOcur[w] += 1
                else:
                    wordOcur.update({w: 1})

        for link in sc.find_all('a', {'href': True}, recursive=True):
            if link["href"][:5] != "#cite":
                if len(link["href"]) > 5 and "/wiki/" in link["href"][:6].lower():
                    print("\t\t\t\t\tLink: https://en.wikipedia.org" +
                          link["href"])
                else:
                    print("\t\t\t\t\tLink:", link["href"])

        sc = sc.find_next_sibling()

    wordOcur = dict(
        sorted(wordOcur.items(), key=lambda x: x[1], reverse=True))

    print("\t\t\tCommon Words:", end=" ")
    i = 1
    for value in wordOcur:
        if value not in stopwords.words('english'):
            print(value, end=" ")
            i += 1
            if i > 3:
                print("")
                break
