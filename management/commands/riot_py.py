from django.conf import settings
import os
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

imports = "from django.utils.translation import gettext_lazy, ngettext_lazy, pgettext_lazy, npgettext_lazy  # noqa"


class Command(BaseCommand):
    """
    A naive approach to fetching translation strings from
    tag files and dumping them into python to be collected
    """

    def handle(self, *args, **options):
        messages = []
        for root, dirs, files in os.walk(settings.BASE_DIR):
            for riot in filter(
                lambda n: n.endswith(".riot") and n != "trans_late.riot", files
            ):

                with open(os.path.join(root, riot)) as fp:
                    soup = BeautifulSoup(fp, "html.parser")
                    for tag in soup.findAll("trans-late"):

                        plural = tag.get("plural")
                        context = tag.get("context")
                        msgid = tag.get("msgid")
                        number = tag.get("number", 1)

                        if context and plural:
                            messages.append(
                                f'''    npgettext_lazy(context="""{context}""", singular="""{msgid}""", plural="""{plural}""", number="""{number}""")'''
                            )

                        elif context:
                            messages.append(
                                f'''    pgettext_lazy(context="""{context}""", message="""{msgid}""")'''
                            )

                        elif plural:
                            messages.append(
                                f'''    ngettext_lazy(singular="""{msgid}""", plural="""{plural}""", number="""{number}""")'''
                            )

                        elif msgid:
                            messages.append(
                                f'''    gettext_lazy(message="""{msgid}""")'''
                            )
        messages = sorted(set(messages))
        with open(
            os.path.join(settings.BASE_DIR, "gettext_utils", "gettext_strings.py"), "w"
        ) as outfile:
            outfile.write(imports)
            outfile.write("\n\n\n")
            outfile.write("def __messages__():\n")
            outfile.write("\n".join(messages))
            outfile.write("\n")
