from django.conf import settings


from .decorators import check_settings

from mastodon import Mastodon


@check_settings
def get_api():
    api = Mastodon(
        access_token=settings.MASTODON_ACCESS_TOKEN,
        api_base_url=settings.MASTODON_API_BASE_URL,
    )
