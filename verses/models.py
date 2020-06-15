from django.db import models
from . import custom_models
from django.contrib.auth import get_user_model

User = get_user_model()

# STATIC TABLES
class Verse(models.Model):
    verse_id = models.CharField(max_length=15,null=False, unique=True, primary_key=True)
    canto_num = models.IntegerField(null=False)
    chapter_num = models.IntegerField(null=False)
    verse_num = models.IntegerField(null=False)
    verse_num_end = models.IntegerField(null=True)
    verse = custom_models.Text(max_length=1000, null=False)
    synonyms = custom_models.Text(max_length=5000, null=False)
    devanagari = custom_models.Text(max_length=1000, null=False)
    translation = custom_models.Text(max_length=1000, null=False)
    purport = custom_models.Text(max_length=40000, null=True)

    context = custom_models.Text(max_length=1000, null=True)
    title = custom_models.Text(max_length=500, null=True)

class Tag(models.Model):
    name = models.CharField(max_length=100, null=False)
    level = models.PositiveSmallIntegerField(default=1, null=False)
    parent = models.ForeignKey('self', default=None, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('level', 'name')

class Tag1(models.Model):
    name = models.CharField(max_length=60, unique=True)

class Tag2(models.Model):
    parent_tag = models.ForeignKey(Tag1, on_delete=models.PROTECT)
    name = models.CharField(max_length=60, unique=True)

class Tag3(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent_tag = models.ForeignKey(Tag2, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.name)

class TranslationTag(models.Model):
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag3, on_delete=models.SET_DEFAULT, default="None")
    tagger = models.ForeignKey(User, related_name="translation_tagger", on_delete=models.SET_NULL, null=True)
    tagger_remark = models.CharField(max_length=1000, null=True)
    reviewer = models.ForeignKey(User, related_name="translation_reviewer", on_delete=models.SET_NULL, null=True)
    tag_name = models.ForeignKey(Tag, on_delete=models.SET_DEFAULT, default="None")

    class Meta:
        unique_together = ('verse_id', 'tag')

class PurportSectionTag(models.Model):
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)
    start_idx = models.IntegerField(null=False)
    end_idx = models.IntegerField(null=False)
    tag = models.ForeignKey(Tag3,on_delete=models.SET_DEFAULT, default="None")
    tagger = models.ForeignKey(User, related_name="purport_tagger", on_delete=models.SET_NULL, null=True)
    tagger_remark = models.CharField(max_length=1000, null=True)
    reviewer = models.ForeignKey(User, related_name="purport_reviewer", on_delete=models.SET_NULL, null=True)
    tag_name = models.ForeignKey(Tag, on_delete=models.SET_DEFAULT, default="None")

    class Meta:
        unique_together = ('verse_id', 'tag', 'start_idx', 'end_idx')

class TagRequest(models.Model):
    verse_id = models.CharField(max_length=15,null=False, unique=True, primary_key=True)
    name = models.CharField(max_length=70)
    parent = models.CharField(max_length=60)
    description = models.CharField(max_length=1000, null=True)
    initiator = models.ForeignKey(User, related_name="tagrequest_initiator", on_delete=models.SET_NULL, null=True)
    approver = models.ForeignKey(User, related_name="tagrequest_approver", on_delete=models.SET_NULL, null=True)
