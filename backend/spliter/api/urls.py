from django.urls import path

from .views import SplitView

app_name = "splits"
urlpatterns = [path("split/", SplitView.as_view(), name="split")]
