from django.conf import settings
import os
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from itertools import chain

imports = "from django.utils.translation import gettext_lazy, ngettext_lazy, pgettext_lazy, npgettext_lazy  # noqa"


def get_riot_files():
    """
    Generator returning all of the files ending in ".riot"
    within the current project

    Yields:
        [str]: A path to the filenale
    """
    for root, _, files in os.walk(settings.BASE_DIR):
        for riotfile in filter(
            lambda n: n.endswith(".riot") and n != "trans_late.riot", files
        ):
            yield os.path.join(root, riotfile)


def process_tag(tag):
    """
    Returns a fragment of Python code representing a translation
    which is extracted from a "trans-late" tag
    """

    plural = tag.get("plural").replace('"', '"') if tag.get("plural") else None
    context = tag.get("context").replace('"', '"') if tag.get("context") else None
    msgid = tag.get("msgid").replace('"', '"') if tag.get("msgid") else None
    number = tag.get("number", 1) if tag.get("number") else None
    comment = "#" if "{" in msgid else ""

    if context and plural:
        return f"""{comment}npgettext_lazy(context="{context}", singular="{msgid}", plural="{plural}", number="{number}")"""
    elif context:
        return f"""{comment}pgettext_lazy(context="{context}", message="{msgid}")"""
    elif plural:
        return f"""{comment}ngettext_lazy(singular="{msgid}", plural="{plural}", number="{number}")"""
    elif msgid:
        return f"""{comment}gettext_lazy(message="{msgid}")"""


class Command(BaseCommand):
    """
    A naive approach to fetching translation strings from
    tag files and dumping them into python to be collected
    """

    def handle(self, *args, **options):
        verbosity = options.get("verbosity")
        output = os.path.join(settings.BASE_DIR, "gettext_utils", "gettext_strings.py")
        preamble = f"{imports}\n\n\ndef __messages__():"
        postamble = "\n"
        with open(output, "w") as outfile:
            outfile.write(preamble)
            for riot in get_riot_files():
                with open(riot) as fp:
                    # Scan the riot file for trans-late tags and anything which uses `is="trans-late"` syntax
                    soup = BeautifulSoup(fp, "html.parser")
                    # Extract a set of "translations" from the file
                    tags = {
                        t
                        for t in [
                            process_tag(tag)
                            for tag in chain(
                                soup.find_all("trans-late"),
                                soup.find_all(attrs={"is": "trans-late"}),
                            )
                        ]
                        if not t.startswith("#")
                    }
                if tags:
                    # Verbose explain to the user what we're picking up here
                    if verbosity > 0:
                        self.stdout.write(
                            self.style.SUCCESS(f"{riot}: {len(tags)} translations")
                        )
                    if verbosity > 1:
                        for t in tags:
                            self.stdout.write(self.style.SUCCESS(f"{t}"))
                    header = f"\n\n\t# {riot}\n\t"
                    tagstrings = "\n\t".join(tags)
                    # Indicate the file location
                    outfile.write(header)
                    # Write python-code strings for gettext & related functions
                    outfile.write(tagstrings)
            outfile.write(postamble)  # For pep8, empty line at end of file
