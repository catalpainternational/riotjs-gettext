from django.contrib import admin

from .models import Translatable, Translated

# Register your models here.


class TranslatedInline(admin.TabularInline):
    model = Translated


@admin.register(Translatable)
class TranslatableAdmin(admin.ModelAdmin):
    list_display = [
        "msgid",
        "msgid_plural",
        "msgctxt",
        "comment",
        "tcomment",
        "occurences",
        "flags",
        "previous_msgctxt",
        "previous_msgid",
        "previous_msgid_plural",
        "linenum",
    ]

    inlines = [TranslatedInline]


@admin.register(Translated)
class TranslatedAdmin(admin.ModelAdmin):
    list_display = [
        "msg",
        "msgstr",
        "msgstr_plural",
        "obsolete",
        "language",
    ]
