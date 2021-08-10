import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

words_display = 5  # number of popular words to show

# use this instead for user input for words amount
# print("Number of words to display:", end=" ")
# words_display=input()


print("Wikipedia Article Link:", end=" ")
response = requests.get(
    url=input()
)
print('\n')

soup = BeautifulSoup(response.content, 'lxml')

title = soup.find(id="firstHeading")
print("Article:", title.text)

# gets every section component
sections = soup.select_one(".mw-parser-output").findChildren(recursive=False)

# removes Navigation Box elements
for rmv in sections:
    if rmv.has_attr('id') and (rmv['id'] == 'toc'):
        sections.remove(rmv)
        break

# dictionary for storing word occurences per section
words = dict()

for sect in sections:
    # "mw-headline" are section headings
    if sect.find(class_="mw-headline"):
        # sorts dictionary based on occurrence (value)
        words = dict(
            sorted(words.items(), key=lambda x: x[1], reverse=True))

        print("\t\tCommon Words:", end=" ")
        i = 1
        # prints and dumps words from dictionary because of new section start
        for value in words:
            if value not in stopwords.words('english'):
                print(value, end=" ")
                i += 1
                if i > words_display:
                    print("")
                    break

        words.clear()

        # quits on References
        if sect.find(class_="mw-headline").text == "References":
            exit()

        text = sect.find(class_="mw-headline").text
        if sect.name == "h2":
            print("Section:", text)
        else:
            print("\tSub-Section:", text)
    else:

        # cleans up text references
        text = sect.text
        text = text.replace('(', '').replace(')', '').replace(',', '')
        text = text.split()

        # updates word occurrences in dictionary
        for word in text:
            word = word.lower()
            if word in words:
                words[word] += 1
            else:
                words.update({word: 1})

        # find all links and prints
        links = sect.find_all('a', {'href': True}, recursive=True)
        if links != None:
            for link in links:
                if link["href"][0] != "#" and link["href"][-11:] != "action=edit":
                    if len(link["href"]) > 5 and "/wiki/" in link["href"][:6].lower():
                        # Refactors Wikipedia article links
                        print("\t\t\t\t\tLink: https://en.wikipedia.org" +
                              link["href"])
                    else:
                        print("\t\t\t\t\tLink:", link["href"])
