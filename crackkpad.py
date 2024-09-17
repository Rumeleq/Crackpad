import subprocess
import sys
import os
import re
try:
    import requests
except ImportError:
    print("Instaluję paczkę requests... ")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Instaluję paczkę beautifulsoup4...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
    from bs4 import BeautifulSoup


class TextColors:
    PURPLE = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    ERROR = "\033[91m"
    ENDCOLOR = "\033[0m"

# https://www.wattpad.com/1288484961-%E2%9C%85zakazana-studentka-18%2B-rozdzia%C5%82-6


def wycionk_z_altoreczki(link_list):
    chapter_regex1 = re.compile(r"-\d+$", re.IGNORECASE)
    chapter_regex_page = re.compile(r"-\d+/page/\d+$", re.IGNORECASE)
    for link in link_list:
        print(link)
        if chapter_regex_page.search(link):
            chapter_number = link[link.rfind("-")+1:link.rfind("/page/")]
        elif chapter_regex1.search(link):
            chapter_number = link[link.rfind("-")+1:]
        else:
            chapter_number = "#"
        fanfik = requests.get(link, headers=headers)
        
        if fanfik.status_code == 200:
            dzieuo = BeautifulSoup(fanfik.text, "html.parser")

            pre_elements = dzieuo.find_all("pre")
            for i, pre in enumerate(pre_elements):
                p_elements = pre.find_all("p")
                text = ""
                
                for p in p_elements:
                    text += p.get_text() + "\n"

                output_filename = f"chapter {chapter_number}.txt"
                with open(output_filename, "a", encoding="utf-8") as f:
                    f.write(text)
                    
                print(f"{TextColors.GREEN}Zakończono ekstrakcję{TextColors.ENDCOLOR} z <pre> nr {i + 1} z linku: {TextColors.PURPLE}{link}{TextColors.ENDCOLOR}. Zapisano w: {TextColors.YELLOW}{os.getcwd() + "\\" + output_filename}{TextColors.ENDCOLOR}")
        else:
            print(f"{TextColors.ERROR}Dupa, coś się wysypało: {TextColors.ENDCOLOR}{fanfik.status_code}")


url_list = []
link_number = 1
url_regex = re.compile(r"^https?://")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
while True:
    try:
        NFZ = (input(f"Podaj {link_number} link rozdziału do odczytania lub rozpocznij kradzież fanfika wprowadzając \"quit\": ")).lower()
        if NFZ == "quit":
            break
        elif url_regex.match(NFZ):
            url_list.append(NFZ)
            page_number = 1
            while True:
                page_number += 1
                page_link = NFZ + f"/page/{page_number}"
                response = requests.get(page_link, headers=headers)
                first_p = BeautifulSoup(response.text, "html.parser").select_one("pre > p")

                if first_p is None:
                    break
                if response.status_code == 200:
                    url_list.append(page_link)

            link_number += 1
        else:
            print(f"{TextColors.ERROR}Coś ci nie wyszło z tym linkiem - spróbuj się zacząć od https:// lub http://{TextColors.ENDCOLOR}")
    except Exception as ex:
        print(f"{TextColors.ERROR}Wystąpił nieoczekiwany błąd: {TextColors.ENDCOLOR}{ex}")
    
wycionk_z_altoreczki(url_list)
