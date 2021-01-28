
from django.urls import path
from . import views

urlpatterns = [
    #login, registration
    path('login/', views.loginView, name="login"),
    path('register/', views.registerView, name="register"),
    path('logout/', views.logoutView, name="logout"),
    path('changePaSs/', views.password_change.as_view(), name='change_password'),
    #non-registered user
    path('', views.indexView.as_view(), name = "home"),
    path('service/', views.serviceView.as_view(), name="service"),
    path('advice/', views.adviceView.as_view(), name="advice"),
    path('about-us/', views.aboutUSView.as_view(), name="about_us"),
    path('contact/', views.contactView.as_view(), name="contact"),
    path('documentation/', views.Documentation.as_view(), name="Documentation"),
]
