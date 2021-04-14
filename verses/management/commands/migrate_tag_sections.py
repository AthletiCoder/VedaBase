from django.core.management.base import BaseCommand
from django.conf import settings
import os, json
from verses.models import Tag1, Tag2, Tag3, Tag, PurportSectionTag, TranslationTag
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class Command(BaseCommand):
    help = "To migrate tag data from 3-level tags to multi-level tags"

    def handle(self, *args, **kwargs):
        for t_tag in TranslationTag.objects.all():
            print(t_tag.tag.name)
            t_tag.tag_name = Tag.objects.get(name=t_tag.tag.name, level=3)
            t_tag.save()

        for p_tag in PurportSectionTag.objects.all():
            print(t_tag.tag.name)
            p_tag.tag_name = Tag.objects.get(name=p_tag.tag.name, level=3)
            p_tag.save()

