from django.contrib import admin

from .models import Toot
from .models import TootFile
from .models import TootPublication


admin.site.register(Toot)
admin.site.register(TootFile)
admin.site.register(TootPublication)
