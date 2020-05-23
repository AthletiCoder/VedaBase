from django.core.management.base import BaseCommand
from django.conf import settings
import os, json, re
from verses.models import Verse

class Command(BaseCommand):
    help = 'Fill database with verses data from vedabase.io'

    def handle(self, *args, **kwargs):
        import json
        from bs4 import BeautifulSoup
        import requests

        def next_url(soup):
            next_button = [btn for btn in soup.find_all('a', {'class':'btn'}) if 'Next' in btn.text]
            return next_button[0]['href']

        def tweak_url(url):
            if url.endswith("/1/"):
                return url[:-1]+"-2/"
            if "/1-" in url:
                return url[:-2]+str(int(url[-2])+1)+"/"

        def get_element(soup, name):
            elements = soup.findAll('div', name)
            conc = "\n".join([str(obj) for obj in elements])
            chosen = re.sub('<br/s*?>', '\n', conc)
            html_chosen = BeautifulSoup(chosen, 'html.parser')
            return html_chosen.get_text()

        def touch_up(url):
            return url+(10-len(url.split("/")))*"1/"

        def get_verse_details(url):
            r = requests.get(url)
            soup = BeautifulSoup(r.content,'html.parser')
            canto, chapter, verse, _ = url.split('/')[-4:]
            request_body = {
                'verse_id' : canto+"."+chapter+"."+verse,
                'devanagari': get_element(soup, 'r-devanagari'),
                'verse': get_element(soup,'r-verse-text'),
                'synonyms': get_element(soup, 'r-synonyms'),
                'translation': get_element(soup, 'r-translation'),
                'purport': get_element(soup, 'r-paragraph'),
                'canto_num': int(canto),
                'chapter_num': int(chapter)
            }
            if '-' in verse:
                verse_details = verse.split("-")
                request_body["verse_num"] = int(verse_details[0])
                request_body["verse_num_end"] = int(verse_details[1])
            else:
                request_body["verse_num"] = int(verse)
            return request_body, soup

        # Main command block
        current_url = "https://vedabase.io/en/library/sb/1/1/1/"

        while True:
            try:
                request_body, soup = get_verse_details(current_url)
            except:
                print("Skipping url:", current_url)
                current_url = tweak_url(current_url)
                continue
            if request_body["translation"]!='':
                try:
                    Verse.objects.create(**request_body)
                    print("Successfully added verse:", request_body["verse_id"])
                except:
                    print("Failed to create verse:", request_body["verse_id"])
            current_url = "https://vedabase.io"+next_url(soup)
            current_url = touch_up(current_url)