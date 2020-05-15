from .models import Verse, TranslationTag, PurportSectionTag, Tag1, Tag2, Tag3

from marshmallow import Schema, fields

class VerseSchema(Schema):
    model = Verse

    verse_id = fields.Str(required=True)
    canto_num = fields.Integer(required=True)
    chapter_num = fields.Integer(required=True)
    verse_num = fields.Integer(required=True)
    verse = fields.Str(required=True)
    translation = fields.Str(required=True)
    purport = fields.Str(required=True)

class TagSchema(Schema):
    tag1 = fields.Str(required=False)