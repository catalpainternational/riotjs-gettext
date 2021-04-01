
from django.db import models
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import Concat
from django.db.models.expressions import Case, F, Value, When
import json
import polib

import os
from bs4 import BeautifulSoup

class TranslationSourceQuerySet(models.QuerySet):

    def catalog(self, language):
        """
        Group all of the "plural" forms into an array compatible with gettext JS functions
        """
        return self.filter(translatedmessage__language = language).values('msgid').annotate(
            msg_with_context = Case (
            When (
                context__isnull = True, then=F('msgid')
            ),
            When(context__isnull=False, then=Concat(F('context'), Value(r'\x04'),F('msgid')))
        )).values('msg_with_context').annotate(
            texts = ArrayAgg('translatedmessage__msgstr',ordering=F('translatedmessage__msgstr_plurality'))).values('msg_with_context', 'texts')

    def catalog_as_dict(self, language):
        return {
            i['msg_with_context']: i['texts'] if len(i['texts']) > 1 else i['texts'][0] for i in self.catalog(language)
        }

    def catalog_as_po(self, language, output_path):
        po = polib.POFile()
        for entry in self.filter(translatedmessage__language = language).values('msgid', 'translatedmessage__msgstr'):
            entry_po = polib.POEntry(
                msgid = entry['msgid'],
                msgstr = entry['translatedmessage__msgstr']
            )
            po.append(entry_po)
        po.save(output_path)

class TranslationSource(models.Model):
    """
    A "Translated" string
    """
    msgid = models.CharField(max_length=512, help_text="The message text to translate from")
    comment_for_translators = models.CharField(max_length=2000, null=True, blank=True)
    context = models.CharField(max_length=512, help_text="Optional context marker for the message", null=True, blank=True)

    objects = TranslationSourceQuerySet.as_manager()

    def __str__(self):
        return self.msgid


class TranslatedMessage(models.Model):
    msg = models.ForeignKey(TranslationSource, on_delete = models.CASCADE)
    msgstr = models.CharField(max_length=512)
    msgstr_plurality = models.IntegerField(null=True, blank=True, help_text="Which plural form this translation refers to, 0 is singular, 1 is more than one (en). Other languages may have more forms.", default=0)
    language = models.CharField(max_length=5)

    def __str__(self):
        return self.msgstr

    def interpolate(self, *args):
        return self.msgstr.format(args)

    def named_interpolate(self, **kwargs):
        return self.msgstr % (kwargs)

    @classmethod
    def from_po_content(cls, po_path: str, lc: str):
        """
        Read content of a .po file into the database
        """
        po = polib.pofile(po_path)
        valid_entries = [e for e in po if not e.obsolete]
        for entry in valid_entries:
            print(entry.msgid, entry.msgstr)
            ts = TranslationSource.objects.get_or_create(
                msgid = entry.msgid,
                context = entry.msgctxt
            )[0]
            cls.objects.get_or_create(
                msg=ts,
                msgstr=entry.msgstr,
                language=lc
            )

    def to_po_entry(self):
        return polib.POEntry(
            msgid=self.msg.msgid,
            msgstr=self.msgstr
        )
