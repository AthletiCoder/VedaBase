from django.contrib import admin
from .models import Verse, TranslationTag, PurportSectionTag, Tag
from django.contrib.auth.models import Group
admin.site.register([Verse, TranslationTag, PurportSectionTag])

class TagA(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent_id', 'level')
    list_filter = ('parent_id','level')
    search_fields = ('name','parent_id')
    ordering = ('id', 'parent_id', 'name', 'level')
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(Tag, TagA)
