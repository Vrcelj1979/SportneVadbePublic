from google.cloud import ndb
from models.db_settings import get_db

client = get_db()


class CompanyWorkout(ndb.Model):
    workout_id = ndb.IntegerProperty()
    company_id = ndb.IntegerProperty()
    contract_number = ndb.IntegerProperty()
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
