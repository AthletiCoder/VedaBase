import os, json, re
import json
from bs4 import BeautifulSoup
import requests
from verses.models import Verse, PurportSectionTag

def next_url(soup):
    next_button = [btn for btn in soup.find_all('a', {'class':'btn'}) if 'Next' in btn.text]
    return next_button[0]['href']

def tweak_url(url):
    if url.endswith("/1/"):
        return url[:-1]+"-2/"
    if "/1-" in url:
        return url[:-2]+str(int(url[-2])+1)+"/"

def dollar(purport, verse):
    start = purport.find(verse)
    return purport[:start]+"$$"+verse+"$$"+purport[start+len(verse):]

def get_purport(soup, name):
    elements = soup.findAll('div', name)
    verse_refs = elements[0].findAll('div','r-verse-text')
    verse_refs = [re.sub('<br/s*?>','\n',str(verse_ref)) for verse_ref in verse_refs]
    verse_refs = [BeautifulSoup(verse,'html.parser').get_text() for verse in verse_refs]
    conc = "\n".join([str(obj) for obj in elements])
    chosen = re.sub('<br/s*?>', '\n', conc)
    html_chosen = BeautifulSoup(chosen, 'html.parser')
    purport = html_chosen.get_text()
    for verse_ref in verse_refs:
        purport = dollar(purport, verse_ref)
    return purport.strip('\n').strip('Purport').strip('\n')

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
        'verse': get_element(soup,'wrapper-verse-text').strip('Text').strip('\n'),
        'synonyms': get_element(soup, 'r-synonyms'),
        'translation': get_element(soup, 'r-translation'),
        'purport': get_purport(soup, 'wrapper-puport'),
        'canto_num': int(canto),
        'chapter_num': int(chapter)
    }
    if '-' in verse:
        verse_details = verse.split("-")
        request_body["verse_num"] = int(verse_details[0])
        request_body["verse_num_end"] = int(verse_details[1])
    else:
        request_body["verse_num"] = int(verse)
        request_body["verse_num_end"] = int(verse)
    return request_body, soup

def modify_verse(verse_id):
    base_url = "https://vedabase.io/en/library/sb/"
    url = base_url + verse_id.replace('.','/') + "/"
    req, _ = get_verse_details(url)
    new_verse = req['verse'].strip('\n').strip('Text').strip('\n')
    new_purport = req['purport'].strip('\n').strip('Purport').strip('\n')
    
    all_p_tags = PurportSectionTag.objects.filter(verse__verse_id=verse_id)
    for p_tag in all_p_tags:
        section = verse.purport[p_tag.start_idx:p_tag.end_idx+1]
        section_length = p_tag.end_idx-p_tag.start_idx+1
        new_start_idx = new_purport.find(section)
        new_end_idx = new_start_idx+section_length-1
        PurportSectionTag.objects.filter(tag_id=p_tag.tag_id).update(start_idx=new_start_idx, end_idx=new_end_idx)

    Verse.objects.filter(verse_id=verse_id).update(verse=new_verse,purport=new_purport)

def modify_db():
    all_verses = Verse.objects.all()
    for verse in all_verses:
        verse_id = verse.verse_id
        modify_verse(verse_id)

url = "https://vedabase.io/en/library/sb/3/7/3/"
req, soup = get_verse_details(url)
