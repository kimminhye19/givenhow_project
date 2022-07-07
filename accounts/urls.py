from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup),
    path('new_login/', views.new_login),
    path('existing_login/', views.existing_login),
    path('logout/', views.logout),
]