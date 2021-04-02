from django.utils.translation import (
    gettext_lazy,
    ngettext_lazy,
    npgettext_lazy,
    pgettext_lazy,
)  # noqa

gettext_lazy("""Activity""")
gettext_lazy("""General""")
gettext_lazy("""Project""")
gettext_lazy("""{ tab[1].label }""")
ngettext_lazy("""I caught %s pocket monster!. Remaining: %s""", """?""", 1)
ngettext_lazy("""There is %(total)s object. Remaining: %(count)s""", """?""", 1)
ngettext_lazy("""There is one activity""", """There are many activities""", 1)
npgettext_lazy(
    """bar""", """There is one activity""", """There are many activities""", 1
)
npgettext_lazy(
    """foo""", """There is one activity""", """There are many activities""", 1
)
pgettext_lazy("""animal""", """Elephant""")
pgettext_lazy("""editor""", """%(project_or_activity)s Description""")
pgettext_lazy("""editor""", """%(project_or_activity)s Objectives""")
pgettext_lazy("""editor""", """%(project_or_activity)s Partner ID""")
pgettext_lazy("""editor""", """%(project_or_activity)s Status""")
pgettext_lazy("""editor""", """%(project_or_activity)s Target Groups""")
pgettext_lazy("""editor""", """%(project_or_activity)s Title""")
pgettext_lazy(
    """editor""",
    """A detailed description of the %s objectives and its expected outcomes.""",
)
pgettext_lazy("""editor""", """Collaboration Type""")
pgettext_lazy(
    """editor""", """Details of groups that are intended to benefit from the %s."""
)
pgettext_lazy("""editor""", """Expected Finish Date""")
pgettext_lazy("""editor""", """Expected Start Date""")
pgettext_lazy("""editor""", """Save and Next""")
pgettext_lazy("""editor""", """Save""")
pgettext_lazy("""editor""", """Sector""")
pgettext_lazy(
    """editor""",
    """This explains what the %s is, it’s longer than the title and contains more detail.""",
)
pgettext_lazy("""month""", """Elephant""")
pgettext_lazy("""month""", """may""")
pgettext_lazy("""verb""", """may""")
