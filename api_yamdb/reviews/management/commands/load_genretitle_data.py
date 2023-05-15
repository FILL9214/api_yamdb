from csv import DictReader
from typing import Any
from django.core.management import BaseCommand
from reviews.models import GenreTitle

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from genretitle.csv"

    def handle(self, *args: Any, **options):
        if GenreTitle.objects.exists():
            print('genretitle data already loaded...exiting')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        for row in DictReader(open(
                              './static/data/genre_title.csv',
                              encoding="utf-8-sig")):
            genretitle = GenreTitle(
                genre_id=row['genre_id'],
                title_id=row['title_id'])
            genretitle.save()
