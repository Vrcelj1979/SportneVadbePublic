from google.cloud import ndb
from models.db_settings import get_db

client = get_db()


class SportCenter(ndb.Model):
    title = ndb.StringProperty()
    email_address = ndb.StringProperty()
    street = ndb.TextProperty()
    city = ndb.TextProperty()
    zip_number = ndb.StringProperty()
    country = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def create(cls, text):
        with client.context():  # with client.context() is obligatory to use in the new ndb library
            message = cls(text=text)
            message.put()

            return message

    @classmethod
    def fetch_all(cls):
        with client.context():
            messages = cls.query().fetch()

            return messages
