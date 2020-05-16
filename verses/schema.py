from .models import Verse, TranslationTag, PurportSectionTag, Tag1, Tag2, Tag3

from marshmallow import Schema, fields

class VerseSchema(Schema):
    model = Verse

    verse_id = fields.Str(required=True)
    canto_num = fields.Integer(required=False)
    chapter_num = fields.Integer(required=False)
    verse_num = fields.Integer(required=False)
    verse = fields.Str(required=True)
    translation = fields.Str(required=True)
    purport = fields.Str(required=True)

class TagSchema(Schema):
    model = Tag1
    tag1 = fields.Str(required=False)

class TranslationTagSchema(Schema):
    model = TranslationTag

    verse = fields.Str(required=True)
    tag = fields.Str(required=True)

class PurportSectionTagSchema(Schema):
    model = PurportSectionTag

    verse = fields.Str(required=True)
    start_idx = fields.Integer(required=True)
    end_idx = fields.Integer(required=True)
    tag = fields.Str(required=True)