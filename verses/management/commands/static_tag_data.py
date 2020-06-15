from django.core.management.base import BaseCommand
from django.conf import settings
import os, json
from verses.models import Tag1, Tag2, Tag3
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Fill DB with static data'

    def handle(self, *args, **kwargs):
        with open(os.path.join(settings.BASE_DIR, 'static_tag_data.json')) as file_handler:
            data = json.load(file_handler)
            all_tags = data["outline"]
            for tag1_data in all_tags:
                tag1 = tag1_data["text"]
                try:
                    tag1_obj = Tag1.objects.get_or_create(name=tag1)
                except (ValidationError, IntegrityError) as e:
                    print("Tag 1 getting/fetching failed:", e)
                all_tag2_data = tag1_data["outline"]
                for tag2_data in all_tag2_data:
                    tag2 = tag2_data["text"]
                    if isinstance(tag1_obj, tuple):
                        tag1_obj = tag1_obj[0]
                    try:
                        tag2_obj = Tag2.objects.get_or_create(parent_tag=tag1_obj,name=tag2)
                    except (ValidationError, IntegrityError) as e:
                        print("Tag 2 getting/fetching failed:", e)
                    all_tag3_data = tag2_data["outline"]
                    for tag3_data in all_tag3_data:
                        tag3 = tag3_data["text"]
                        if isinstance(tag2_obj, tuple):
                            tag2_obj = tag2_obj[0]
                        try:
                            Tag3.objects.get_or_create(parent_tag=tag2_obj,name=tag3)
                        except (ValidationError, IntegrityError) as e:
                            print("Tag 3 getting/fetching failed:", e)
