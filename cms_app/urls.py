from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('deatils/', views.UserDetailsView.as_view(), name="deatils"),
    path('deatils/<int:pk>', views.UserDetailsView.as_view(), name="deatils"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
