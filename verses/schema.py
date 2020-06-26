from .models import Verse, TranslationTag, PurportSectionTag, Tag
from marshmallow import Schema, fields, validates, ValidationError, validates_schema, validate

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

    context = fields.Str(dump_only=True)
    title = fields.Str(dump_only=True)

class BaseTaggingSchema(Schema):
    tag_id = fields.Function(lambda obj: obj.id)
    verse_id = fields.Str(required=True)
    tag = fields.Str(required=True, load_only=True)
    tag_name = fields.Function(lambda obj:obj.tag_name.name, dump_to="tag", dump_only=True)
    tagger = fields.Function(lambda obj: obj.tagger.email if obj.tagger!=None else None, dump_only=True, dump_to="tagger")
    tagger_remark = fields.Str(required=False)
    reviewer = fields.Function(lambda obj: obj.reviewer.email if obj.reviewer!=None else None, dump_only=True, dump_to="reviewer")

    @validates("verse_id")
    def validate_verse_id(self, value):
        verse_obj = Verse.objects.filter(verse_id=value)
        if not verse_obj:
            raise ValidationError("Invalid verse_id")

    @validates("tag")
    def validate_tag(self, value):
        tag_obj = Tag.objects.filter(name=value)
        if not tag_obj:
            raise ValidationError("Invalid tag")
        if not tag_obj[0].is_leaf:
            raise ValidationError("Not a leaf tag")

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

class AdditionalDetailsSchema(Schema):
    verse_id = fields.Str(required=True)
    context = fields.Str(required=False, validate=validate.Length(max=1000))
    title = fields.Str(required=False, validate=validate.Length(max=500))

    @validates("verse_id")
    def validate_verse_id(self, value):
        verse_obj = Verse.objects.filter(verse_id=value)
        if not verse_obj:
            raise ValidationError("Invalid verse_id")
