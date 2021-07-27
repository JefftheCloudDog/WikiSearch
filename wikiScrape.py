import urllib
import requests
from bs4 import BeautifulSoup, Tag
from nltk.corpus import stopwords
from collections import Counter

response = requests.get(
    url="https://en.wikipedia.org/wiki/Dog"
)

print("Code:", response.status_code)

soup = BeautifulSoup(response.content, 'lxml')


# mv-headline: section titles(includes subsections)
# --- if p follows mv-headline(h2 or h3) it is part of that section

title = soup.find(id="firstHeading")
print("Article:", title.text)


# title2 = soup.find("h3")
# print(title2.find(id="Domestication"))
# print(title2.next_sibling)

# ERROR: Navigable string -> use nextElement(?)

# cltur k c/u
headers = soup.select(".mw-headline")
stop_words = set(stopwords.words('english'))


for sc in headers[:1]:
    sc = sc.parent

    if sc.parent.name == "h2":
        print("\tSection:", sc.text)
    elif sc.text.lower() == "references" or sc.text.lower == "reference":
        break
    else:
        print("\t\tSub-Section:", sc.text)

    sc = sc.find_next_sibling()

    wordOcur = dict()
    while sc.find(class_="mw-headline") == None:
        if len(sc.text) > 0:
            print("\t\t\t\tText:", sc.text)
            # do word analysis

            text = sc.text
            text = text.split()

        for link in sc.find_all('a', recursive=True):
            if link.parent.name != "sup":
                if len(link["href"]) > 5 and "/wiki/" in link["href"][:6].lower():
                    print("\t\t\t\t\tLink: https://en.wikipedia.org" +
                          link["href"])
                else:
                    print("\t\t\t\t\tLink:", link["href"])

        # print out word occurences

        sc = sc.find_next_sibling()
