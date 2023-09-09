from django.contrib import admin


from .models import DjangoNewsIssue
from .models import DjangoNewsIssueItem


@admin.register(DjangoNewsIssue)
class DjangoNewsIssueAdmin(admin.ModelAdmin):
    list_display = ("__str__", "date", "url")
    list_filter = ("date",)
    readonly_fields = ("title", "date", "url")


@admin.register(DjangoNewsIssueItem)
class DjangoNewsIssueItemAdmin(admin.ModelAdmin):
    list_display = ("__str__", "category", "url", "url_status_code")
    list_filter = ("category", "url_status_code")
