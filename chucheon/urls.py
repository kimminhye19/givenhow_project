from django.urls import path
from . import views

app_name = 'chucheon'
urlpatterns = [
    path('survey/', views.survey_view),
    path('result/', views.getAiResult),
    path('like1/', views.getAiResult_like1),
    path('like2/', views.getAiResult_like2),
    path('like3/', views.getAiResult_like3),
]