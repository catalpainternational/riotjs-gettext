from typing import ContextManager
from django.conf import settings
import os
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils.translation import npgettext

imports = "from django.utils.translation import gettext_lazy, ngettext_lazy, pgettext_lazy, npgettext_lazy  # noqa"

class Command(BaseCommand):
    """
    A naive approach to fetching translation strings from
    tag files and dumping them into python to be collected
    """
    def handle(self, *args, **options):

        messages = [imports]

        for root, dirs, files in os.walk(settings.BASE_DIR):
            for riot in filter(lambda n: n.endswith('.riot') and n != 'trans_late.riot', files):

                with open(os.path.join(root, riot)) as fp:
                    soup = BeautifulSoup(fp, 'html.parser')
                    for tag in soup.findAll('trans-late'):

                        plural = tag.get('plural')
                        context = tag.get('context')
                        msgid = tag.get('msgid')

                        if context and plural:
                            messages.append(f'''npgettext_lazy("""{context}""", """{msgid}""", """{plural}""", 1)''')

                        elif context:
                            messages.append(f'''pgettext_lazy("""{context}""", """{msgid}""")''')

                        elif plural:
                            messages.append(f'''ngettext_lazy("""{msgid}""", """{plural}""", 1)''')

                        elif msgid:
                            messages.append(f'''gettext_lazy("""{msgid}""")''')
        messages = sorted(set(messages))
        with open(os.path.join(settings.BASE_DIR, 'gettext_utils', 'gettext_strings.py'), 'w') as outfile:
            outfile.write('\n'.join(messages))
