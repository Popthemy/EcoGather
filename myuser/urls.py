from django.urls import path
from . import views

urlpatterns = [
    path('register/',view=views.RegisterView.as_view(),name='register_user'),
    path('login/',view=views.LoginView.as_view(),name='login_user'),
    path('logout/',view=views.LogoutView.as_view(),name='logout_user'),
    path('refresh/',view=views.TokenRefreshView.as_view(),name='token_refresh'),
]
