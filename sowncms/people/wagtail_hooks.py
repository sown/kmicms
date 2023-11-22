from wagtail.snippets.models import register_snippet

from .views import DegreeViewSetGroup, PersonViewSet

# Viewsets
register_snippet(DegreeViewSetGroup)
register_snippet(PersonViewSet)
