from django.core.management.base import BaseCommand
from django.conf import settings
import os, json
from verses.models import Tag1, Tag2, Tag3

class Command(BaseCommand):
    help = 'Fill DB with static data'

    def handle(self, *args, **kwargs):
        with open(os.path.join(settings.BASE_DIR, 'static_tag_data.json')) as file_handler:
            data = json.load(file_handler)
            all_tags = data["outline"]
            for tag1_data in all_tags:
                tag1 = tag1_data["text"]
                try:
                    tag1_obj = Tag1.objects.create(name=tag1)
                    print("Created new tag1 named:",tag1)
                except:
                    print("{} already exists in Tag 1 objects list".format(tag1))
                all_tag2_data = tag1_data["outline"]
                for tag2_data in all_tag2_data:
                    tag2 = tag2_data["text"]
                    try:
                        tag2_obj = Tag2.objects.create(parent_tag=tag1_obj,name=tag2)
                        print("Created new tag2 named:",tag2)
                    except:
                        print("{} already exists in Tag 2 objects list".format(tag2))
                    all_tag3_data = tag2_data["outline"]
                    for tag3_data in all_tag3_data:
                        tag3 = tag3_data["text"]
                        try:
                            Tag3.objects.create(parent_tag=tag2_obj,name=tag3)
                            print("Created new tag3 named:",tag3)
                        except:
                            print("{} already exists in Tag 3 objects list".format(tag3))

        
            