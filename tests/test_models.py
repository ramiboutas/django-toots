from pathlib import Path

from django.utils import timezone
from django.conf import settings
from django.core.files.base import ContentFile


from django_tweets.models import Tweet
from django_tweets.models import TweetFile
from django_tweets.models import TweetPublication

from unittest_parametrize import parametrize
from unittest_parametrize import ParametrizedTestCase


now = timezone.now()
now_tupple_6 = (now.year, now.month, now.day, now.hour, now.minute, now.second)
now_str = "%s-%s-%s %s:%s:%s" % now_tupple_6


class TweetModelTests(ParametrizedTestCase):
    def setUp(self):
        # Setup run before every test method.
        Tweet.objects.all().delete()
        TweetFile.objects.all().delete()
        TweetPublication.objects.all().delete()

    def tearDown(self):
        # Clean up run after every test method.
        Tweet.objects.all().delete()
        TweetFile.objects.all().delete()
        TweetPublication.objects.all().delete()

    def test_create_and_delete_tweet(self):
        text = "%s Testing django-tweets." % now_str
        tweet = Tweet.objects.create(text=text)
        published_tweet = tweet.publish()
        published_tweet.delete()

    @parametrize(
        ("extension", "expected"),
        [
            ("gif", True),
            ("jpg", True),
            # ("mp4", True), # not working
            ("png", True),
        ],
    )
    def test_mediafiles(self, extension: str, expected: bool):
        path = Path(settings.BASE_DIR / "tests" / "samples" / f"sample.{extension}")
        with open(path, "rb") as f:
            f.seek(0)
            contents = f.read()
        mediafile = TweetFile.objects.create(title="nice photo")
        mediafile.file.save(path.name, ContentFile(contents))
        mediafile = mediafile.upload()
        tweet = Tweet.objects.create(
            text="%s Testing a tweet with a %s file" % (now_str, extension)
        )
        tweet.files.add(mediafile)
        tweet.publish()
        tweet.delete()
