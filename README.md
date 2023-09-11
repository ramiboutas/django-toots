# django-toots

Create and delete toots in a Django project.

This package takes advantage of the [Mastodon.py](https://pypi.org/project/Mastodon.py/) functionalities to connect it to a Django Backend.



## Set up


1. Install from PyPI
```
python -m pip install django-toots
```

2. Add the package to your settings INSTALLED_APPS

```python

INSTALLED_APPS = [
    ...
    "django_toots",
    ...
]

```


3. Add the following settings to your Django project.


Example:

```python
import os
from dotenv import load_dotenv
load_dotenv()

...

# django-toots 
MASTODON_ACCESS_TOKEN=os.environ.get("MASTODON_ACCESS_TOKEN", "") 
MASTODON_API_BASE_URL = "https://fosstodon.org"

```

4. Run migrations

```
python manage.py migrate

```


## Usage

TODO: Document this!




### Create a simple toot

```python

from django_toots.models import Toot

# create a toot in the db
t = Tweet.objects.create(text="Hi, this is my toot using django-toots and Mastodon.py")

# publish it
t.publish()

```

<!-- 
### Create a tweet with a media file

```python
from pathlib import Path
from django.core.files.base import ContentFile
from django_tweets.models import Tweet, TweetFile

# create a media file
path = Path("path/to/my/file.jpg")

with open(path, "rb") as f:
    f.seek(0)
    contents = f.read()

tweet_file = TweetFile.objects.create(title="nice photo")
tweet_file.file.save(path.name, ContentFile(contents))
# upload to Twitter
tweet_file = tweet_file.upload()

# create a tweet in the db
tweet = Tweet.objects.create(text="My tweet with a file")

# add the media file to the tweet object
tweet.files.add(tweet_file)

# publish it
tweet.publish()

```

### Usage in the admin

![Django admin](images/admin.png)

* Use [http://127.0.0.1:8000/admin/django_tweets/tweet/](http://127.0.0.1:8000/admin/django_tweets/tweet/) to create a Tweet object
* Use [http://127.0.0.1:8000/admin/django_tweets/tweetpublication/](http://127.0.0.1:8000/admin/django_tweets/tweetpublication/) to link a Tweet object to publish it.

Similarly works with the `TweetFile` and `TweetFileUpload` models.



## About

[🐣 django_tweets](https://twitter.com/django_tweets)

©Django is a registered trademark of the Django Software Foundation.
-->