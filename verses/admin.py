from django.contrib import admin
from .models import Verse, TranslationTag, PurportSectionTag, Tag

admin.site.register([Verse, TranslationTag, PurportSectionTag, Tag])


# Register your models here.
