from csv import DictReader
from typing import Any
from django.core.management import BaseCommand
from reviews.models import Title, Category

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from titles.csv"
    categories = Category.objects.all()

    def handle(self, *args: Any, **options):
        if Title.objects.exists():
            print('titles data already loaded...exiting')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        for row in DictReader(open(
                              './static/data/titles.csv',
                              encoding="utf-8-sig")):
            title = Title(
                name=row['name'],
                year=row['year'],
                category_id=row['category'])
            title.save()
