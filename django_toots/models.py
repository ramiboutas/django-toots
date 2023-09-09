import tempfile

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property

from django.conf import settings

from .clients import get_v2_client
from .clients import get_v1dot1_api


def _upload_path(_, filename):
    now = timezone.now()
    return f"django-tweets/{now.year}/{now.month}/{now.day}/{filename}"


class TweetFile(models.Model):
    title = models.CharField(
        _("Title"),
        max_length=128,
        blank=True,
    )
    file = models.FileField(
        _("File"),
        upload_to=_upload_path,
    )
    delete_after_upload = models.BooleanField(
        _("Delete the file after upload"),
        default=False,
    )
    created_at = models.DateTimeField(
        _("Created at"),
        editable=False,
        blank=True,
        auto_now_add=True,
    )
    expires_at = models.DateTimeField(
        _("Expires at"),
        editable=True,
        blank=True,
        null=True,
    )
    media_id_string = models.CharField(
        max_length=32,
        editable=False,
        blank=True,
        null=True,
    )
    response = models.TextField(
        _("Tweepy Response"),
        editable=True,
        blank=True,
        null=True,
    )

    def upload(self):
        # use tempfile to upload the file to the Twitter API.
        # Why tempfile? because not allways media files are not stored locally
        with tempfile.NamedTemporaryFile(suffix="." + self.file_extension) as f:
            f.write(self.file.read())
            f.seek(0)  # https://github.com/tweepy/tweepy/issues/1667
            response = get_v1dot1_api().chunked_upload(f.name)
        # save values into the db
        self.media_id_string = response.media_id_string
        self.response = str(response)
        self.expires_at = timezone.now() + timezone.timedelta(
            seconds=response.expires_after_secs
        )
        if self.delete_after_upload:
            self.file.delete()
        self.save()
        return self

    @cached_property
    def file_extension(self):
        return self.file.name.split(".")[1]

    def save(self, *args, **kwargs):
        # generate title from file name if not provided
        if self.title == "" or self.title is None:
            self.title = self.file.name
        super(TweetFile, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Tweet(models.Model):
    text = models.TextField(max_length=4096)
    id_string = models.CharField(
        max_length=32,
        editable=False,
        blank=True,
        null=True,
    )
    edit_history_tweet_ids = models.TextField(
        max_length=512,
        editable=False,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    files = models.ManyToManyField(TweetFile, blank=True)
    response = models.TextField(
        _("Tweepy Response"),
        editable=True,
        blank=True,
        null=True,
    )

    def delete(self, *args, **kwargs):
        if getattr(settings, "DJANGO_TWEETS_SYNC_DELETE", True):
            get_v2_client().delete_tweet(self.id_string)
        super(Tweet, self).delete(*args, **kwargs)

    def get_media_ids(self):
        if self.files.all().count() > 0:
            return [f.media_id_string for f in self.files.all()]

    def publish(self):
        # requesting
        response = get_v2_client().create_tweet(
            text=self.text,
            media_ids=self.get_media_ids(),
        )
        # updating the instance from the response
        self.id_string = response.data.get("id")
        self.text = response.data.get("text")
        self.edit_history_tweet_ids = ", ".join(
            response.data.get("edit_history_tweet_ids")
        )
        self.response = str(response)
        self.save()
        return self

    def __str__(self) -> str:
        return "%s %s" % (self.id_string, self.text)


class TweetPublication(models.Model):
    """
    A Model to handle Tweet publication in Django Admin.
    """

    tweet = models.OneToOneField(Tweet, on_delete=models.CASCADE)
    publish = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.publish:
            self.tweet.publish()
        super(TweetPublication, self).save(*args, **kwargs)


class TweetFileUpload(models.Model):
    """
    A Model to handle MediaFile upload in Django Admin.
    """

    mediafile = models.OneToOneField(TweetFile, on_delete=models.CASCADE)
    upload = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.publish:
            self.mediafile.upload()
        super(TweetFileUpload, self).save(*args, **kwargs)



## toots:::


class Toot(models.Model):
    # TODO: create django-toots package
    mastodon_id = models.BigIntegerField()
    url = models.URLField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    replies_count = models.PositiveIntegerField(null=True)
    reblogs_count = models.PositiveIntegerField(null=True)
    favourites_count = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return self.content


## Create a post

def create_post(self, text, filepath: Path = None):
    parameters = {"status": text}
    if filepath:
        media_response = self.api.media_post(filepath)
        parameters["media_ids"] = [media_response.id]
    response = self.api.status_post(**parameters)

