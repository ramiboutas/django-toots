from django.contrib import admin

from .models import TweetFile
from .models import TweetFileUpload
from .models import Tweet
from .models import TweetPublication


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    """
    ModelAdmin for Tweet

    """

    list_display = ("__str__", "id_string", "created_at")
    list_filter = ("created_at",)
    readonly_fields = ("id_string", "edit_history_tweet_ids", "created_at", "response")
    filter_horizontal = ("files",)


@admin.register(TweetFile)
class TweetFileAdmin(admin.ModelAdmin):
    """
    ModelAdmin for MediaFile
    """

    list_display = ("title", "file", "created_at", "expires_at")
    list_filter = ("expires_at", "expires_at")
    readonly_fields = ("created_at", "expires_at", "media_id_string", "response")


@admin.register(TweetPublication)
class TweetPublicationAdmin(admin.ModelAdmin):
    """
    ModelAdmin for TweetPublication
    """

    list_display = ("tweet", "publish")
    list_filter = ("publish",)


@admin.register(TweetFileUpload)
class TweetFileUploadAdmin(admin.ModelAdmin):
    """
    ModelAdmin for MediaFileUpload
    """

    list_display = ("mediafile", "upload")
    list_filter = ("upload",)
