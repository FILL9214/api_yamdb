from csv import DictReader
from typing import Any
from django.core.management import BaseCommand
from reviews.models import Comment

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from comments.csv"

    def handle(self, *args: Any, **options):
        if Comment.objects.exists():
            print('genre data already loaded...exiting')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        for row in DictReader(open(
                              './static/data/comments.csv',
                              encoding="utf-8-sig")):
            comment = Comment(
                review_id=row['review_id'],
                author_id=row['author'],
                text=row['text'],
                pub_date=row['pub_date'])
            comment.save()
