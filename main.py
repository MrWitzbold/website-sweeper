from requests_html import HTMLSession
from bs4 import BeautifulSoup
import time
from lxml import html

def get_srcs(source_str):
    source_str.replace("\n", "")
    src_list = source_str.split("src")
    src_list_ = []
    for i in range(0, len(src_list)):
        if i % 2 != 0:
            possible_link = src_list[i].replace('="', "").split('"')[0]
            if "\\\\" not in possible_link:
                src_list_.append(possible_link)
    return src_list_

website = "https://www.gov.br/"
session = HTMLSession()
r = session.get(website)
source = r.content
soup = BeautifulSoup(str(source), 'html.parser')
links = html.fromstring(str(source)).xpath('//a/@href')
links2 = get_srcs(str(source))
#for link in links2:
#    links.append(link)
file = open("data.txt", "a", encoding="utf-8")

#print("hrefs: " + str(links))
print("\n\nsrc's: " + str(links2))
#print("\n\n" + str(source))

processed_links = []
processed_links.append(website)

def process_links(links):
    for link in links:
        time.sleep(0.5)
        r = session.get(website)
        r.html.render()
        links = r.html.absolute_links
