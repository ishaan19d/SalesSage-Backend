from mongoengine import Document, StringField, DateTimeField
import datetime

class CompanyUser(Document):
    name = StringField(max_length=100)
    username = StringField(max_length=100, unique=True)
    email = StringField(unique=True)
    password = StringField(max_length=100)
    created_at = DateTimeField(default=datetime.datetime.now)

    def is_authenticated(self):
        return True