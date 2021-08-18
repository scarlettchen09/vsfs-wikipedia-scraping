from bs4 import BeautifulSoup
import requests
import re
import sys

DEFAULT_URL = "https://en.wikipedia.org/wiki/Embassy_of_the_United_States,_London"
DEFAULT_LENGTH = 10


def get_all_links_in_section(section):
    list = []
    for link in section.find_all("a"):
        list.append(link.get('href'))
    return list


def get_wikipedia_page(url):
    # Store as (header_name, most common words, links list) tuple pair in list:
    text_and_links_under_headers = []
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    soup = BeautifulSoup(r.text, 'html.parser')

    all_headers = re.compile('^h[2-6]$')
    remove_tags_regex = re.compile("\[.*?\]") # remove [edit] tags on certain pages
    print("********")
    print("Title of page:", soup.find_all("h1")[0].get_text())
    print("********")
    
    for header in soup.find_all(all_headers):
        text_under_header = ""
        links_list = []

        header_text = re.sub(remove_tags_regex, "", header.get_text().rstrip())

        section_text = header

        while True:
            section_text = section_text.next_sibling

            if section_text: # Check not None
                tag_name = section_text.name

                if tag_name == 'p':
                    text_under_header += section_text.get_text()
                    links_list = get_all_links_in_section(section_text)

                elif tag_name == 'ul' or tag_name == 'ol':
                    for li in section_text.find_all('li'):
                        text_under_header += section_text.get_text()
                        links_list = get_all_links_in_section(section_text)

                elif header_text == "References" and tag_name == 'div':
                    text_under_header += section_text.get_text()
                    links_list = get_all_links_in_section(section_text)

                elif all_headers.match(str(tag_name)):
                    break

            else:
                break
        text_and_links_under_headers.append((header_text, find_most_common_words(text_under_header), links_list))
    return text_and_links_under_headers


def process_stop_words(file_name):
    file = open(file_name, 'r')
    stop_words = [word.rstrip() for word in file]
    return stop_words


def find_most_common_words(str):
    stop_words_list = process_stop_words('stopwords.txt')
    words_arr = str.split()
    frequency_dict = {}
    alpha_only_regex = re.compile("[^a-zA-Z]")
    for word in words_arr:
        word = word.lower()
        word = re.sub(alpha_only_regex, "", word)
        if len(word) > 1 and word not in stop_words_list:
            if word in frequency_dict:
                frequency_dict[word] += 1
            else:
                frequency_dict[word] = 1
    frequency_dict_sorted = sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)
    return frequency_dict_sorted


def print_data_for_header(el, number_of_common_words):
    print("Header name:", el[0])
    if len(el[1]) == 0:
        print("No words found under header")
    else:
        if number_of_common_words < len(el[1]):
            print("Most common words:", el[1][:number_of_common_words])
        else:
            print("Most common words:", el[1])
    if len(el[2]) == 0:
        print("No links found under header")
    else:
        print("Links found under header", el[2])
    print('\n')


def output_results(data, ignore_empty_headers, number_of_common_words):
    if not ignore_empty_headers:
        for el in data:
            print_data_for_header(el, number_of_common_words)
    else:
        for el in data:
            if len(el[1]) != 0 or len(el[2]) != 0:
                print_data_for_header(el, number_of_common_words)
            

if __name__ == '__main__':
    n = len(sys.argv)
    url = DEFAULT_URL
    length = DEFAULT_LENGTH
    ignore_empty_headers = True

    print("num of args passed:", n)
    if n == 1:
        pass
    elif n == 2:
        url = str(sys.argv[1])
    elif n == 4:
        if str(sys.argv[3]).lower() == "false" or str(sys.argv[3]).lower() == "no":
            ignore_empty_headers = False
    else:
        url = str(sys.argv[1])
        try:
            length = int(sys.argv[2])
        except ValueError:
            print("Invalid length received, setting to default")
            length = DEFAULT_LENGTH
        if length <= 0:
            print("Invalid length received, setting to default")
            length = DEFAULT_LENGTH

    results = get_wikipedia_page(url)
    output_results(results, ignore_empty_headers, length)