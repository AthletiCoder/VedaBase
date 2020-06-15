from django.core.management.base import BaseCommand
from django.conf import settings
import os, json
from verses.models import Tag1, Tag2, Tag3, Tag, PurportSectionTag, TranslationTag
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class Command(BaseCommand):
    help = "To migrate tag data from 3-level tags to multi-level tags"

    def handle(self, *args, **kwargs):
        all_tag3 = Tag3.objects.all()
        all_tag2 = Tag2.objects.all()
        all_tag1 = Tag1.objects.all()

        for tag1 in all_tag1:
            kwargs = dict()
            kwargs["name"] = tag1.name
            kwargs["level"] = 1
            tag1_obj = Tag.objects.create(**kwargs)
            for tag2 in all_tag2.filter(parent_tag__name=tag1_obj.name):
                kwargs = dict()
                kwargs["name"] = tag2.name
                kwargs["level"] = 2
                kwargs["parent"] = tag1_obj
                tag2_obj = Tag.objects.create(**kwargs)
                for tag3 in all_tag3.filter(parent_tag__name=tag2_obj.name):
                    kwargs = dict()
                    kwargs["name"] = tag3.name
                    kwargs["level"] = 3
                    kwargs["parent"] = tag2_obj
                    tag3_obj = Tag.objects.create(**kwargs)

        for t_tag in TranslationTag.objects.all():
            t_tag.tag_name = Tag.objects.filter(name=t_tag.tag.name)
            t_tag.save()

        for p_tag in PurportSectionTag.objects.all():
            p_tag.tag_name = Tag.objects.filter(name=p_tag.tag.name)
            p_tag.save()


