from marshmallow import Schema, fields


class ErrorResponseSchema(Schema):
    msg = fields.Raw()
