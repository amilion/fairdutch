from rest_framework import routers
from .views import DutchViewSet

router = routers.SimpleRouter()
router.register(r"dutches", DutchViewSet, basename="dutches")

app_name = "dutches"
urlpatterns = [] + router.urls
