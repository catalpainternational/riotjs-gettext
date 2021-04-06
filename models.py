from django.db import models

class TranslationTargetQuerySet(models.Manager):

    def catalog(self):
        """

        """
        # Group all of the "plural" forms into an array
        pass


class TranslationSource(models.Model):
    """
    A "Translated" string may include
    """
    msgid = models.CharField(max_length=512, help_text="The message text to translate from", unique=True)
    msgid_plural = models.CharField(max_length=512, help_text="Optional plural form of the message")
    comment_for_translators = models.CharField(max_length=2000)


class TranslatedMessage(models.Model):
    msg = models.ForeignKey(TranslationSource)
    msgstr = models.CharField(max_length=512)
    msgstr_plurality = models.IntegerField(nunll=True, blank=True, help_text="Which plural form this translation refers to")
    language = models.CharField(max_length=5)


class CommonText(models.Model):
    """
    Holds translations of common components which may be renamed between
    projects. For example a mohinga 'Activity' is a Dird 'Project' and a Hamutuk 'Program'.
    """
    concept = models.CharField(max_length=128)
    description = models.TextField()
    translated_string = models.ForeignKey(TranslationSource, to_field='msgid')
