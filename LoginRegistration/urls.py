from django.urls import path, include
from LoginRegistration import views
from SongSuggestion.views import detect_emotion
from SongSuggestion import urls


urlpatterns = [
    path("", views.home, name='home'),
    path("register/", views.RegisterView, name="register"),
    path("login/", views.LoginView , name="login"),
    path("logout/", views.LogoutView , name="logout"),
    path('forgot-password/', views.ForgotPasswordView, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.ResetPasswordSentView, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.ResetPasswordView, name='reset-password'),
    path('redirect-to-emotion/', views.redirecttosongmodule, name='redirect_to_emotion'),
    path('playsongs/',views.playsongs, name='playsongs'),

    #--ADMIN URLS--#
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manage_playlists/', views.manage_playlists, name='manage_playlists'),

    path('add_playlist/', views.add_playlist, name='add_playlist'),
    path('update_playlist/<int:id>/', views.update_playlist, name='update_playlist'),
    path('delete_playlist/<int:id>/', views.delete_playlist, name='delete_playlist'),
    path('get_languages/', views.get_languages, name='get_languages'),

    path("manage_users/", views.manage_users, name="manage_users"),
    #path("add_user/", views.add_user, name="add_user"),
    path("update_user/<int:id>/", views.update_user, name="update_user"),
    path("delete_user/<int:id>/", views.delete_user, name="delete_user"),

    path('submit/', views.submit_feedback, name='submit_feedback'),
    path('manage_feedback/', views.manage_feedback, name='manage_feedback'),
    path('update_feedback/<int:feedback_id>/', views.update_feedback, name='update_feedback'),
    path('delete_feedback/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
    
]
