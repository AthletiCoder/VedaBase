from django.contrib import admin
from .models import Verse, TranslationTag, PurportSectionTag, Tag1, Tag2, Tag3
from django.contrib.auth.models import Group
admin.site.register([Verse, TranslationTag, PurportSectionTag])


# Register your models here.

class Tag1A(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    ordering = ('id', 'name',)
    filter_horizontal = ()

class Tag2A(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent_tag_id')
    list_filter = ('parent_tag_id',)
    search_fields = ('name','parent_tag_id')
    ordering = ('id', 'parent_tag_id', 'name')
    filter_horizontal = ()
     
class Tag3A(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent_tag_id')
    list_filter = ('parent_tag_id',)
    search_fields = ('name','parent_tag_id')
    ordering = ('id', 'parent_tag_id', 'name')
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(Tag1, Tag1A)
admin.site.register(Tag2, Tag2A)
admin.site.register(Tag3, Tag3A)
