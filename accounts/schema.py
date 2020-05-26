from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

class RegisterSchema(Schema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    user_type = fields.String(validate=validate.OneOf(['user','tagger','reviewer']))