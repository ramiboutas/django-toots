from django.conf import settings

from mastodon import Mastodon

from .decorators import check_settings


@check_settings
def get_api():
    return Mastodon(
        access_token=settings.MASTODON_ACCESS_TOKEN,
        api_base_url=settings.MASTODON_API_BASE_URL,
    )
