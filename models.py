from typing import Dict, List, Union

import polib
from django.contrib.postgres.fields import ArrayField
from django.db import models

Catalog = Dict[str, Union[str, List[str]]]


class TranslatableQuerySet(models.QuerySet):
    def catalog_as_dict(self, language="en"):
        cat = {}
        for entry in self.filter(translated__language=language).values(
            "msgctxt", "msgid", "translated__msgstr", "translated__msgstr_plural"
        ):
            k = (
                f"{entry['msgctxt']}\x04{entry['msgid']}"
                if entry["msgctxt"]
                else f"{entry['msgid']}"
            )
            v = (
                entry["translated__msgstr_plural"]
                if entry["translated__msgstr_plural"]
                else entry["translated__msgstr"]
            )
            if v:
                cat[k] = v
        return cat

    def catalog_as_po(self, language="en"):
        po = polib.POFile()
        for entry in self.filter(translated__language=language).select_related("msg"):
            po.append(entry.to_po_entry)
        return self.__unicode__()


class Translatable(models.Model):
    """
    A "Translatable" string.
    """

    msgid = models.CharField(
        max_length=512, help_text="The message text to translate from"
    )
    msgid_plural = ArrayField(
        models.CharField(
            max_length=512, help_text="The message text to translate for a plural case"
        ),
        null=True,
        blank=True,
    )
    msgctxt = models.CharField(
        max_length=512,
        help_text="Optional context marker for the message",
        null=True,
        blank=True,
    )

    # Comments can be added to assist translators.
    # Some comments are automatically added by gettext utilities.
    comment = models.CharField(
        max_length=512, blank=True, null=True, help_text="Extracted comments"
    )
    tcomment = models.CharField(
        max_length=512, blank=True, null=True, help_text="Translator comments"
    )

    occurences = ArrayField(
        models.CharField(
            max_length=512,
            blank=True,
            null=True,
            help_text="Describe where this occurs",
        ),
        blank=True,
        null=True,
    )
    flags = ArrayField(
        models.CharField(max_length=128),
        blank=True,
        null=True,
    )

    # If a string is marked as "fuzzy" these can help to determine
    # the original translation
    previous_msgctxt = models.CharField(max_length=512, blank=True, null=True)
    previous_msgid = models.CharField(max_length=512, blank=True, null=True)
    previous_msgid_plural = models.CharField(max_length=512, blank=True, null=True)

    linenum = models.IntegerField(blank=True, null=True)

    objects = TranslatableQuerySet.as_manager()

    def __str__(self):
        return self.msgid


class Translated(models.Model):
    """
    Relates a translation in a given language to a translatable string
    """

    msg = models.ForeignKey(Translatable, on_delete=models.CASCADE)
    msgstr = models.CharField(
        max_length=512, help_text="The translation of the entry message string"
    )
    msgstr_plural = ArrayField(models.CharField(max_length=512), null=True, blank=True)
    obsolete = models.BooleanField(null=True, blank=True)
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
            ts = Translatable.objects.get_or_create(
                msgid=entry.msgid, msgctxt=entry.msgctxt
            )[0]
            cls.objects.get_or_create(msg=ts, msgstr=entry.msgstr, language=lc)

    def to_po_entry(self):
        return polib.POEntry(
            msgid=self.msg.msgid,
            msgstr=self.msgstr,
            msgid_plural=self.msgid_plural,
            msgctxt=self.msg.msgctxt,
            obsolete=self.obsolete,
        )
