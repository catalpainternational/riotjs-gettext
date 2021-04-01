from django.contrib import admin
from . import models
# Register your models here.


class TranslatedMessageInline(admin.TabularInline):
    model = models.TranslatedMessage

@admin.register(models.TranslationSource)
class TranslationSourceAdmin(admin.ModelAdmin):
    list_display = ['context', 'msgid', 'comment_for_translators']
    inlines = [TranslatedMessageInline]

@admin.register(models.TranslatedMessage)
class TranslatedMessageAdmin(admin.ModelAdmin):
    list_display = ['msg', 'msgstr', 'msgstr_plurality', 'language']
