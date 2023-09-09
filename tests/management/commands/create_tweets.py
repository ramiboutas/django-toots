from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q


from django_tweets.models import Tweet
from tests.models import DjangoNewsIssueItem


class Command(BaseCommand):
    help = "Publishes a Tweet object"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--deleteprevious",
            action="store_true",
            help="Delete Tweets before creating",
        )

    def handle(self, *args, **options):
        self.stdout.write("Starting...")

        if options["deleteprevious"]:
            Tweet.objects.all().delete()

        # Creating from Django-News items
        issue_items = DjangoNewsIssueItem.objects.filter(
            Q(category="Articles") | Q(category="Tutorials"),
            url_status_code=200,
        )
        tweets = []
        for item in issue_items:
            tweets.append(
                Tweet(
                    text=f"{item.title}\n\n{item.text}\n\n{item.url}\n\n[Credits: Django News]"
                )
            )

        Tweet.objects.bulk_create(tweets)

        self.stdout.write("Done!")
