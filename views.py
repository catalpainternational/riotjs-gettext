from typing import Dict, List, Set, Union
from django.http.response import JsonResponse
from django.utils.translation.trans_real import DjangoTranslation
import json
# from django.utils.translation import gettext, ngettext, pgettext, npgettext
from django.utils import translation
from django.views.i18n import JavaScriptCatalog
import itertools

# magic gettext number to separate context from message
CONTEXT_SEPARATOR = "\x04"


class CatalogView(JavaScriptCatalog):

    domain = 'django'

    """
    Fetch Django's catalog view; but return only the
    requested translation strings
    """

    def get_catalog(self, strings: Set[str] = []) -> Dict[str, Union[List[str], str]]:
        pdict = {}
        num_plurals = self._num_plurals
        catalog = {}
        trans_cat = self.translation._catalog
        trans_fallback_cat = self.translation._fallback._catalog if self.translation._fallback else {}
        seen_keys = set()
        for key, value in itertools.chain(trans_cat.items(), trans_fallback_cat.items()):
            if key == '' or key in seen_keys or key not in strings:
                continue
            if isinstance(key, str):
                catalog[key] = value
            elif isinstance(key, tuple):
                msgid, cnt = key
                pdict.setdefault(msgid, {})[cnt] = value
            else:
                raise TypeError(key)
            seen_keys.add(key)
        for k, v in pdict.items():
            # Adds plural form translations
            catalog[k] = [v.get(i, '') for i in range(num_plurals)]

        return catalog

    def post(self, *args, **kwargs):

        locale = translation.get_language()
        domain = kwargs.get('domain', self.domain)
        # If packages are not provided, default to all installed packages, as
        # DjangoTranslation without localedirs harvests them all.
        packages = kwargs.get('packages', '')
        packages = packages.split('+') if packages else self.packages
        paths = self.get_paths(packages) if packages else None
        self.translation = DjangoTranslation(locale, domain=domain, localedirs=paths)

        body = json.loads(self.request.body)
        if 'language' in body:
            translation.activate(body.get('language'))
        # Broadly speaking, go from 'most complex' to 'least complex' case
        strings = set()
        for msg in body.get('translations'):
            string = msg.get('singular', msg.get('message'))
            context = msg.get('context', None)
            strings.add(F'{context}{CONTEXT_SEPARATOR}{string}' if context else string)

        return JsonResponse({
            'catalog': self.get_catalog(strings)
        })
