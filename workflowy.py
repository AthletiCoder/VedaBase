import json
from bs4 import BeautifulSoup
from verses.models import Verse, TranslationTag, PurportSectionTag

def clean_purport(purport):
    return BeautifulSoup(purport, "html.parser").get_text()

with open('test_workflowy.json', 'r') as f:
    workflowy_json = json.load(f)
    all_cantos = workflowy_json["body"]["outline"]
    for canto in all_cantos:
        canto_num = int(canto["_text"].strip("Canto "))
        all_chapters = canto["outline"]
        for chapter in all_chapters:
            chapter_num = int(chapter["_text"].strip("Chapter "))
            all_assignments = chapter["outline"]
            for assignment in all_assignments:
                user = assignment["_text"].split(" ")[0].strip("@")
                all_verses = assignment["outline"]
                for verse in all_verses:
                    all_tag_work = verse["outline"]
                    translation_tags = None
                    verse_id = None
                    purport = None
                    for tag_work in all_tag_work:
                        if "Purport" in tag_work["_text"]:
                            ctx = {}
                            if not verse_id:
                                purport_section = tag_work["outline"][0]["_text"]
                                verse_obj = Verse.objects.filter(purport__contains=purport_section, chapter_num=chapter_num, canto_num=canto_num)
                                if verse_obj:
                                    ctx["verse"] = verse_obj
                                    verse_id = verse_obj.verse_id
                                    purport = verse_obj.purport
                            ctx["start_idx"] = purport.find(purport_section)
                            ctx["end_idx"] = ctx["start_idx"]+len(purport_section)
                            for t in tag_work["outline"][1:]:
                                tag = t["_text"]
                                no_tags = tag.count("#")
                                if no_tags==0:
                                    continue
                                elif no_tags>1:
                                    tag_group = tag.split(" ")
                                    for ta in tag_group:
                                        try:
                                            ctx["tag"] = Tag3.objects.get(name=ta.strip(" ").strip("#").replace("_", " "))
                                            PurportSectionTag.objects.create(**ctx)
                                        except:
                                            print("Failed to add new purport section")
                                elif no_tags==1:
                                    try:
                                        ctx["tag"] = Tag3.objects.get(name=tag.strip(" ").strip("#").replace("_", " "))
                                        PurportSectionTag.objects.create(**ctx)
                                    except:
                                        print("Failed to add new purport section")
                        if "verse" in tag_work["_text"].lower():
                            translation_tags = tag_work["outline"]