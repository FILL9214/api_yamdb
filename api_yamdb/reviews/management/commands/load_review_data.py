from csv import DictReader
from typing import Any
from django.core.management import BaseCommand
from reviews.models import Review

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from review.csv"

    def handle(self, *args: Any, **options):
        if Review.objects.exists():
            print('review data already loaded...exiting')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        for row in DictReader(open(
                              './static/data/review.csv',
                              encoding="utf-8-sig")):
            review = Review(
                title_id=row['title_id'],
                author_id=row['author'],
                text=row['text'],
                pub_date=row['pub_date'],
                score=row['score'])
            review.save()
