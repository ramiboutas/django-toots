from django.conf import settings

from .exceptions import SettingError


def check_settings(func):
    settings_to_check = (
        "MASTODON_ACCESS_TOKEN",
        "MASTODON_API_BASE_URL",
    )

    def wrapper(*args, **kwargs):
        for setting in settings_to_check:
            if getattr(settings, setting, None) is None:
                raise SettingError("Please provide a setting value to %s" % setting)
        return func(*args, **kwargs)

    return wrapper
