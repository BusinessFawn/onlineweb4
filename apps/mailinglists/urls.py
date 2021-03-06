from django.conf.urls import url

from apps.api.utils import SharedAPIRootRouter
from apps.mailinglists import views

urlpatterns = [url(r"^$", views.index, name="mailinglists_index")]


router = SharedAPIRootRouter()
router.register(
    "mailinglists/groups", views.MailGroupViewSet, basename="mailinglists_groups"
)
router.register(
    "mailinglists/entities", views.MailEntityViewSet, basename="mailinglists_entities"
)
