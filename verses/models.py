from django.db import models
from . import custom_models

# STATIC TABLES

class Verse(models.Model):
    verse_id = models.CharField(max_length=15,null=False, unique=True, primary_key=True)
    canto_num = models.IntegerField(null=False)
    chapter_num = models.IntegerField(null=False)
    verse_num = models.IntegerField(null=False)
    verse = custom_models.Text(max_length=200, null=False)
    translation = custom_models.Text(max_length=1000, null=False)
    purport = custom_models.Text(max_length=40000, null=True)

class Tag1(models.Model):
    name = models.CharField(max_length=20)

class Tag2(models.Model):
    parent_tag = models.ForeignKey(Tag1, on_delete=models.PROTECT)
    name = models.CharField(max_length=20)

class Tag3(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    parent_tag = models.ForeignKey(Tag2, on_delete=models.PROTECT)

class TranslationTag(models.Model):
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag3, on_delete=models.SET_DEFAULT, default="None")

class PurportSectionTag(models.Model):
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)
    start_idx = models.IntegerField(null=False)
    end_idx = models.IntegerField(null=False)
    tag = models.ForeignKey(Tag3,on_delete=models.SET_DEFAULT, default="None")