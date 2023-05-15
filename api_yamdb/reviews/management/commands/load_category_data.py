from csv import DictReader
from typing import Any
from django.core.management import BaseCommand
from reviews.models import Category

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from category.csv"

    def handle(self, *args: Any, **options):
        if Category.objects.exists():
            print('category data already loaded...exiting')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        for row in DictReader(open(
                              './static/data/category.csv',
                              encoding="utf-8-sig")):
            category = Category(name=row['name'], slug=row['slug'])
            category.save()
