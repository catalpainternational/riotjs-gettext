# Generated by Django 3.1.7 on 2021-04-02 04:43

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Translatable",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "msgid",
                    models.CharField(
                        help_text="The message text to translate from", max_length=512
                    ),
                ),
                (
                    "msgid_plural",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            help_text="The message text to translate for a plural case",
                            max_length=512,
                        ),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "msgctxt",
                    models.CharField(
                        blank=True,
                        help_text="Optional context marker for the message",
                        max_length=512,
                        null=True,
                    ),
                ),
                (
                    "comment",
                    models.CharField(
                        blank=True,
                        help_text="Extracted comments",
                        max_length=512,
                        null=True,
                    ),
                ),
                (
                    "tcomment",
                    models.CharField(
                        blank=True,
                        help_text="Translator comments",
                        max_length=512,
                        null=True,
                    ),
                ),
                (
                    "occurences",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            blank=True,
                            help_text="Describe where this occurs",
                            max_length=512,
                            null=True,
                        ),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "flags",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=128),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "previous_msgctxt",
                    models.CharField(blank=True, max_length=512, null=True),
                ),
                (
                    "previous_msgid",
                    models.CharField(blank=True, max_length=512, null=True),
                ),
                (
                    "previous_msgid_plural",
                    models.CharField(blank=True, max_length=512, null=True),
                ),
                ("linenum", models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Translated",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "msgstr",
                    models.CharField(
                        help_text="The translation of the entry message string",
                        max_length=512,
                    ),
                ),
                (
                    "msgstr_plural",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=512),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                ("obsolete", models.BooleanField(blank=True, null=True)),
                ("language", models.CharField(max_length=5)),
                (
                    "msg",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="gettext_utils.translatable",
                    ),
                ),
            ],
        ),
    ]
