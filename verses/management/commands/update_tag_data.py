from django.core.management.base import BaseCommand
from django.conf import settings
import os, json
from verses.models import Tag1, Tag2, Tag3

class Command(BaseCommand):
    help = 'Update existing tags'

    def handle(self, *args, **kwargs):
        with open(os.path.join(settings.BASE_DIR, 'update_tag_data.json')) as file_handler:
            all_updates = json.load(file_handler)
            for update in all_updates:
                old_name = update["old_name"]
                new_name = update["new_name"]
                level = update["tag_level"]
                tag_obj = {1:Tag1,2:Tag2,3:Tag3}
                try:
                    tag_obj[level].objects.filter(name=old_name).update(name=new_name)
                    print("Successfully replaced {} with {} in Tag {} list".format(old_name, new_name, level))
                except:
                    print("Failed to replace {} with {} in Tag {} list".format(old_name, new_name, level))