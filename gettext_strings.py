from django.utils.translation import (
    gettext_lazy,
    ngettext_lazy,
    pgettext_lazy,
    npgettext_lazy,
)  # noqa


def __messages__():

    # resources_table.riot
    gettext_lazy(message="Description")
    gettext_lazy(message="Title")
    gettext_lazy(message="Date Created")

    # contacts.riot
    gettext_lazy(message="Add Contact")
    gettext_lazy(message="Organisation")
    gettext_lazy(message="Contacts")
    gettext_lazy(message="Name")
    gettext_lazy(message="There are no contacts")
    gettext_lazy(
        message="The contacts should include key team members who support this project"
    )
    gettext_lazy(message="Job Title")

    # documents_images.riot
    gettext_lazy(message="Documents and Images")
    gettext_lazy(
        message="Documents and images should include key supporting materials related to this project"
    )
    gettext_lazy(message="Add Document")
    gettext_lazy(message="There are no documents or images uploaded")

    # general.riot
    pgettext_lazy(
        context="editor",
        message="Details of groups that are intended to benefit from the %(project_or_activity)s.",
    )
    pgettext_lazy(context="editor", message="Save")
    gettext_lazy(message="Sector")
    pgettext_lazy(context="editor", message="Expected Finish Date")
    pgettext_lazy(context="editor", message="%(project_or_activity)s Description")
    pgettext_lazy(context="editor", message="Save and Next")
    pgettext_lazy(
        context="editor",
        message="This explains what the %(project_or_activity)s is, it’s longer than the title and contains more detail.",
    )
    pgettext_lazy(context="editor", message="%(project_or_activity)s Objectives")
    pgettext_lazy(
        context="editor",
        message="A detailed description of the %(project_or_activity)s objectives and its expected outcomes.",
    )
    gettext_lazy(message="General")
    pgettext_lazy(context="editor", message="%s Partner ID")
    pgettext_lazy(context="editor", message="Expected Start Date")
    pgettext_lazy(context="editor", message="%(project_or_activity)s Status")
    gettext_lazy(message="Collaboration Type")
    pgettext_lazy(context="editor", message="%(project_or_activity)s Target Groups")
    pgettext_lazy(context="editor", message="%(project_or_activity)s Title")

    # trans_late_example.riot
    pgettext_lazy(context="month", message="Elephant")
    npgettext_lazy(
        context="bar",
        singular="There is one activity",
        plural="There are many activities",
        number="None",
    )
    ngettext_lazy(
        singular="I caught %s pocket monster!. Remaining: %s", plural="?", number="None"
    )
    gettext_lazy(message="Project")
    ngettext_lazy(
        singular="There is %(total)s object. Remaining: %(count)s",
        plural="?",
        number="None",
    )
    pgettext_lazy(context="month", message="may")
    pgettext_lazy(context="animal", message="Elephant")
    npgettext_lazy(
        context="foo",
        singular="There is one activity",
        plural="There are many activities",
        number="None",
    )
    ngettext_lazy(
        singular="There is one activity",
        plural="There are many activities",
        number="None",
    )
    gettext_lazy(message="Activity")
    pgettext_lazy(context="verb", message="may")
