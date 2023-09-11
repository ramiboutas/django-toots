import tempfile

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property

from .api import get_api


def _upload_path(_, filename):
    now = timezone.now()
    return f"django-toots/{now.year}/{now.month}/{now.day}/{filename}"


class TootFile(models.Model):
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
    url = models.URLField(null=True, blank=True, editable=False)

    created_at = models.DateTimeField(
        _("Created at"),
        editable=False,
        blank=True,
        auto_now_add=True,
    )

    response = models.TextField(
        _("Mastodon.py Response"),
        editable=True,
        blank=True,
        null=True,
    )

    @cached_property
    def file_extension(self):
        return self.file.name.split(".")[1]

    def save(self, *args, **kwargs):
        # generate title from file name if not provided
        if self.title == "" or self.title is None:
            self.title = self.file.name
        super(TootFile, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Toot(models.Model):
    text = models.TextField(max_length=4096)
    url = models.URLField(null=True, blank=True, editable=False)
    mastodon_id = models.BigIntegerField(null=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    files = models.ManyToManyField(TootFile, blank=True)
    response = models.TextField(
        _("Mastodon.py Response"),
        editable=True,
        blank=True,
        null=True,
    )

    def publish(self):
        parameters = {"status": self.text}
        api = get_api()
        if hasattr(self, "files"):
            media_ids = []
            for file in self.files.all():
                with tempfile.NamedTemporaryFile(suffix="." + file.file_extension) as f:
                    f.write(file.file.read())
                    f.seek(0)
                    media_response = api.media_post(f.name)
                    media_ids.append(media_response.id)

                    # delete file once uploaded (if specified)
                    if file.delete_after_upload:
                        file.file.delete()
                    # save file obj
                    file.url = media_response.get("url")
                    file.response = str(media_response)
                    file.save()
            parameters["media_ids"] = media_ids
        # creating the post
        response = api.status_post(**parameters)
        self.mastodon_id = response.get("id")
        self.url = response.get("url")
        self.created_at = response.get("created_at")
        self.response = str(response)
        self.save()
        return self

    def __str__(self) -> str:
        return "%s %s" % (self.mastodon_id, self.text)


class TootPublication(models.Model):
    """
    A Model to handle Tweet publication in Django Admin.
    """

    toot = models.OneToOneField(Toot, on_delete=models.CASCADE)
    publish = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.publish:
            self.toot.publish()
        super(TootPublication, self).save(*args, **kwargs)
