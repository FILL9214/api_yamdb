from csv import DictReader
from typing import Any
from django.core.management import BaseCommand
from reviews.models import User

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from users.csv"

    def handle(self, *args: Any, **options):
        if User.objects.exists():
            print('users data already loaded...exiting')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        for row in DictReader(open(
                              './static/data/users.csv',
                              encoding="utf-8-sig")):
            user = User(
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],)
            user.save()
