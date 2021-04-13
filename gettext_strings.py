from django.utils.translation import (
    gettext_lazy,
    ngettext_lazy,
    pgettext_lazy,
    npgettext_lazy,
)  # noqa


def __messages__():

    # /home/josh/github/catalpainternational/openly_mohinga/openly/openly/src/tags/editor/tabs/general.riot
    pgettext_lazy(context="editor", message="%(project_or_activity)s Objectives")
    gettext_lazy(message="General")
    pgettext_lazy(
        context="editor",
        message="Details of groups that are intended to benefit from the %(project_or_activity)s.",
    )
    gettext_lazy(message="Sector")
    pgettext_lazy(context="editor", message="%(project_or_activity)s Status")
    pgettext_lazy(context="editor", message="Expected Start Date")
    pgettext_lazy(
        context="editor",
        message="This explains what the %(project_or_activity)s is, it’s longer than the title and contains more detail.",
    )
    gettext_lazy(message="Collaboration Type")
    pgettext_lazy(context="editor", message="Save and Next")
    pgettext_lazy(context="editor", message="%s Partner ID")
    pgettext_lazy(context="editor", message="%(project_or_activity)s Description")
    pgettext_lazy(context="editor", message="%(project_or_activity)s Title")
    pgettext_lazy(context="editor", message="%(project_or_activity)s Target Groups")
    pgettext_lazy(context="editor", message="Save")
    pgettext_lazy(
        context="editor",
        message="A detailed description of the %(project_or_activity)s objectives and its expected outcomes.",
    )
    pgettext_lazy(context="editor", message="Expected Finish Date")

    # /home/josh/github/catalpainternational/openly_mohinga/gettext_utils/src/tags/trans_late_example.riot
    ngettext_lazy(
        singular="There is one activity",
        plural="There are many activities",
        number="None",
    )
    npgettext_lazy(
        context="foo",
        singular="There is one activity",
        plural="There are many activities",
        number="None",
    )
    gettext_lazy(message="Project")
    npgettext_lazy(
        context="bar",
        singular="There is one activity",
        plural="There are many activities",
        number="None",
    )
    ngettext_lazy(
        singular="I caught %s pocket monster!. Remaining: %s", plural="?", number="None"
    )
    pgettext_lazy(context="animal", message="Elephant")
    gettext_lazy(message="Activity")
    ngettext_lazy(
        singular="There is %(total)s object. Remaining: %(count)s",
        plural="?",
        number="None",
    )
    pgettext_lazy(context="month", message="may")
    pgettext_lazy(context="verb", message="may")
    pgettext_lazy(context="month", message="Elephant")
