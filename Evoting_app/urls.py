from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.index, name="index"),
    path('home',views.index, name="home"),
    path('voterlogin',views.voterlogin, name="voterlogin"),
    path('officerlogin',views.officerlogin, name="officerlogin"),
    path('register',views.register, name="register"),
    path('voting',views.voting, name="voting"),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)