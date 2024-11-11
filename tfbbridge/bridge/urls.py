from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("oauth_callback", views.handle_oauth, name="handle_oauth"),
    path("add/send/<str:url_id>", views.add_sending_group, name="add_sending_group"),
]