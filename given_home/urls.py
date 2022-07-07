from django.urls import path
from . import views

app_name = 'given_home'
urlpatterns = [
    path('', views.General_chucheon),
    path('chucheon_home', views.TripLocal_Chucheon),
    # path('chucheon_home/like1', views.TripLocal_Chucheon_like1),
    # path('chucheon_home/like2', views.TripLocal_Chucheon_like2),
    # path('chucheon_home/like3', views.TripLocal_Chucheon_like3),
]