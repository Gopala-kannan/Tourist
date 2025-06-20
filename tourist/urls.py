from django.urls import path
from tourist import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('destination/', views.destination, name='destination'),
    path('home/', views.home, name='home'),
    path('destination_list/', views.destination_list, name='destination_list'),
    path('destination_detail/<int:id>/', views.destination_detail, name='destination_detail'),
    path('destination_create/', views.destination_create, name='destination_create'),
    path('destination_update/<int:id>/', views.destination_update, name='destination_update'),
    path('destination_delete/<int:id>/', views.destination_delete, name='destination_delete'),
]