from django.contrib import admin
from .models import *
# Register your models here.

class SubjectChaptersAdmin(admin.ModelAdmin):
    search_fields = ('name','code')
admin.site.register(SubjectChapters,SubjectChaptersAdmin)

admin.site.register(Course)

