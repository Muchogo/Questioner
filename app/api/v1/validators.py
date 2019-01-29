
from marshmallow import ValidationError, Schema, fields, ValidationError


def validate_string(s):

    if not s.strip():
        raise ValidationError('Empty string invalid')


class MeetupsSchema(Schema):

    meetupId = fields.Int()
    createdOn = fields.DateTime()
    createdBy = fields.Int(required=True)
    location = fields.Str(required=True)
    comment = fields.Str(required=True)
    status = fields.Str()
    images = fields.List(fields.Str())
    videos = fields.List(fields.Str())


class UserSchema(Schema):

    userid = fields.Int()
    first_name = fields.Str(required=True, validate=validate_string)
    last_name = fields.Str(required=True, validate=validate_string)
    other_names = fields.Str(validate=validate_string)
    phonenumber = fields.Str(required=True, validate=validate_string)
    username = fields.Str(required=True, validate=validate_string)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate_string)
    isAdmin = fields.Bool()
    registeredOn = fields.DateTime()


class MeetupsEditSchema(Schema):
    userid = fields.Int(required=True)
    comment = fields.Str(required=True)
    location = fields.Str(required=True)