from .models import Verse, TranslationTag, PurportSectionTag, Tag1, Tag2, Tag3

from marshmallow import Schema, fields, validates, ValidationError, validates_schema

class VerseSchema(Schema):
    model = Verse

    verse_id = fields.Str(required=True)
    canto_num = fields.Integer(required=False)
    chapter_num = fields.Integer(required=False)
    devanagari = fields.Str(required=True)
    synonyms = fields.Str(required=True)
    verse = fields.Str(required=True)
    translation = fields.Str(required=True)
    purport = fields.Str(required=True)

class TagSchema(Schema):
    model = Tag1
    tag1 = fields.Str(required=False)
    
class BaseTaggingSchema(Schema):
    tag_id = fields.Function(lambda obj: obj.id)
    verse_id = fields.Str(required=True)
    tag = fields.Str(required=True)
    tagger = fields.Function(lambda obj: obj.tagger.username if obj.tagger!=None else None, dump_only=True, dump_to="tagger")
    reviewer = fields.Function(lambda obj: obj.reviewer.username if obj.reviewer!=None else None, dump_only=True, dump_to="reviewer")

    @validates("verse_id")
    def validate_verse_id(self, value):
        verse_obj = Verse.objects.filter(verse_id=value)
        if not verse_obj:
            raise ValidationError("Invalid verse_id")

    @validates("tag")
    def validate_tag(self, value):
        tag_obj = Tag3.objects.filter(name=value)
        if not tag_obj:
            raise ValidationError("Invalid tag")

class TranslationTagSchema(BaseTaggingSchema):
    model = TranslationTag

class PurportSectionTagSchema(BaseTaggingSchema):
    model = PurportSectionTag

    start_idx = fields.Integer(required=True)
    end_idx = fields.Integer(required=True)

    @validates_schema
    def validate_indices(self, data, **kwargs):
        start = int(data.get("start_idx"))
        end = int(data.get("end_idx"))
        verse_id = data.get("verse_id")
        purport_size = len(Verse.objects.get(verse_id=verse_id).purport)
        if start>=end or end>purport_size-1 or start<0:
            raise ValidationError("Invalid start and end indices")