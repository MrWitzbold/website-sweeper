from requests_html import HTMLSession
from bs4 import BeautifulSoup
import time
from lxml import html
import jsbeautifier
import cssbeautifier

def get_srcs(source_str, root_link):
    source_str.replace("\n", "")
    src_list = source_str.split("src")
    src_list_ = []
    for i in range(0, len(src_list)):
        if i % 2 != 0:
            possible_link = src_list[i].replace('="', "").split('"')[0]
            if "\\\\" not in possible_link and " " not in possible_link:
                if "http" not in possible_link:
                    if root_link[len(root_link)-1] == "/":
                        root_link = f"{root_link[0: -1]}"
                    src_list_.append(root_link + possible_link.replace("//", "/"))
                else:
                    src_list_.append(possible_link)
    return src_list_

website = "https://www.gov.br/"
session = HTMLSession()
data_file = open("data.txt", "a", encoding="utf-8")
links_file = open("links.txt", "a", encoding='utf-8')

processed_links = []

def process_links(links):
    for link in links:
        if link not in processed_links and "gov.br" in link:
            try:
                time.sleep(0.5)
                r = session.get(link)
                r.html.render()
                source = r.content

                new_links = html.fromstring(str(source)).xpath('//a/@href')
                new_links2 = get_srcs(str(source), link)
                for src_link in new_links2:
                    new_links.append(src_link)

                print(new_links)
                processed_links.append(link)
                for new_link in new_links:
                    if "gov.br" in new_link:
                        links_file.write("\n" + new_link)
                process_links(new_links)
            except:
                it = 0

process_links([website])
