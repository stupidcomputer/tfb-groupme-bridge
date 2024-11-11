from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('groupme/', include('bridge.urls')),
    path('groupme/admin/', admin.site.urls),
]
