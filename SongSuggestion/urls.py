from django.urls import path
from . import views

urlpatterns = [
    path('emotion/', views.detect_emotion, name='emotion'),
    path('emotion/history/', views.emotion_history_view, name='emotion_history'),
    path("logout/", views.LogoutView , name="logout"),
    path('beatcanvas/', views.beatcanvas, name='beatcanvas'),
    path('add-language/', views.add_language, name='add_language'),
    
]
