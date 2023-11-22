from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import DegreeSubject, DegreeType, Person


class DegreeSubjectViewSet(SnippetViewSet):
    model = DegreeSubject


class DegreeTypeViewSet(SnippetViewSet):
    model = DegreeType

class DegreeViewSetGroup(SnippetViewSetGroup):

    items = (DegreeSubjectViewSet, DegreeTypeViewSet)
    menu_label = "Degree Settings"
    add_to_settings_menu = True

class PersonViewSet(SnippetViewSet):
    model = Person

    icon = "user"
    add_to_admin_menu = True

    list_filter = ["status", "is_active", "radio_licence"]

    panels = [
        FieldRowPanel(
            [
                FieldPanel("name"),
                FieldPanel("nickname"),
            ],
        ),
        FieldPanel("irc_nick"),
        FieldRowPanel(
            [
                FieldPanel("status"),
                FieldPanel("is_active"),
            ],
        ),
        MultiFieldPanel(
            [
                FieldRowPanel([FieldPanel("radio_licence"), FieldPanel("is_radio_instructor")]),
                InlinePanel(
                    "callsigns",
                    heading="Radio Callsigns",
                    label="Callsign",
                    help_text="HAM Radio Callsigns belonging to this person. The first callsign in the list will be assumed to be the usual callsign.",  # noqa: E501
                ),
            ],
            heading="Amateur Radio",
        ),
        InlinePanel("degree_courses", heading="Degree Course(s)", label="Degree"),
    ]
