import random

from django.conf import settings
from django.core.management.base import BaseCommand

from django_tweets.models import Tweet


class Command(BaseCommand):
    help = "Publishes a Tweet object"

    def handle(self, *args, **options):
        self.stdout.write("Publishing tweet...")
        tweets = Tweet.objects.filter(id_string=None)

        if tweets.exists():
            tweet = random.choice(list(tweets))
            tweet.publish()

        self.stdout.write("Done!")
