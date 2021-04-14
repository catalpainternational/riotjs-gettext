from django.utils.translation import (
    gettext_lazy,
    ngettext_lazy,
    pgettext_lazy,
    npgettext_lazy,
)  # noqa


def __messages__():

    # resources_table.riot
    gettext_lazy(message="Description")
    gettext_lazy(message="Date Created")
    gettext_lazy(message="Title")

    # comments.riot
    gettext_lazy(message="Post comment")
    gettext_lazy(message="Comments")
    gettext_lazy(message="Project Log")

    # contacts.riot
    gettext_lazy(message="Mailing Address")
    gettext_lazy(message="There are no contacts")
    gettext_lazy(message="Job Title")
    gettext_lazy(message="Name")
    gettext_lazy(message="Telephone")
    gettext_lazy(message="Person Name")
    gettext_lazy(message="Organisation")
    gettext_lazy(message="Contacts")
    gettext_lazy(message="Add Contact")
    gettext_lazy(
        message="The contacts should include key team members who support this project"
    )
    gettext_lazy(message="Email")

    # documents_images.riot
    gettext_lazy(message="There are no documents or images uploaded")
    gettext_lazy(message="General")
    gettext_lazy(message="Title")
    gettext_lazy(
        message="Documents and images should include key supporting materials related to this project"
    )
    gettext_lazy(message="File URL")
    gettext_lazy(message="Add Document")
    gettext_lazy(message="Documents and Images")
    gettext_lazy(message="Upload Document")
    gettext_lazy(message="Document Description")

    # general.riot
    gettext_lazy(message="General")
    pgettext_lazy(
        context="editor",
        message="The title should be a human readable name of the %(project_or_activity)s. Please ensure that acronyms are fully spelled out.",
    )
    pgettext_lazy(context="editor", message="%(project_or_activity)s Title")
    pgettext_lazy(
        context="editor",
        message="The date on which the %(project_or_activity)s ended, for example the date of the first or last planned disbursement or when physical activity ends.",
    )
    pgettext_lazy(context="editor", message="%(project_or_activity)s Target Groups")
    pgettext_lazy(
        context="editor",
        message="A detailed description of the %(project_or_activity)s objectives and its expected outcomes.",
    )
    pgettext_lazy(
        context="editor",
        message="Details of groups that are intended to benefit from the %(project_or_activity)s.",
    )
    pgettext_lazy(context="editor", message="Save and Next")
    pgettext_lazy(
        context="editor",
        message="The date on which the %(project_or_activity)s started, for example the date of the first or last disbursement or when physical activity started.",
    )
    pgettext_lazy(context="editor", message="Expected Start Date")
    gettext_lazy(message="Sector")
    pgettext_lazy(context="editor", message="Actual End Date")
    pgettext_lazy(
        context="editor",
        message="This explains what the %(project_or_activity)s is, it’s longer than the title and contains more detail.",
    )
    gettext_lazy(message="Collaboration Type")
    pgettext_lazy(
        context="editor",
        message="The date on which the %(project_or_activity)s is planned to start, for example the date of the first or last planned disbursement or when physical activity starts.",
    )
    pgettext_lazy(context="editor", message="%s Partner ID")
    pgettext_lazy(context="editor", message="%(project_or_activity)s Objectives")
    pgettext_lazy(context="editor", message="Actual Start Date")
    pgettext_lazy(
        context="editor",
        message="The date on which the %(project_or_activity)s is planned to end, for example the date of the first or last planned disbursement or when physical activity ends.",
    )
    pgettext_lazy(context="editor", message="%(project_or_activity)s Description")
    pgettext_lazy(context="editor", message="Planned End Date")
    pgettext_lazy(context="editor", message="Save")
    pgettext_lazy(context="editor", message="%(project_or_activity)s Status")

    # trans_late_example.riot
    npgettext_lazy(
        context="foo",
        singular="There is one activity",
        plural="There are many activities",
        number="None",
    )
    gettext_lazy(message="Activity")
    pgettext_lazy(context="verb", message="may")
    pgettext_lazy(context="month", message="may")
    pgettext_lazy(context="animal", message="Elephant")
    ngettext_lazy(
        singular="There is one activity",
        plural="There are many activities",
        number="None",
    )
    ngettext_lazy(
        singular="There is %(total)s object. Remaining: %(count)s",
        plural="?",
        number="None",
    )
    gettext_lazy(message="Project")
    pgettext_lazy(context="month", message="Elephant")
    ngettext_lazy(
        singular="I caught %s pocket monster!. Remaining: %s", plural="?", number="None"
    )
    npgettext_lazy(
        context="bar",
        singular="There is one activity",
        plural="There are many activities",
        number="None",
    )
