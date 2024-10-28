from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api_root'),  # API root endpoint
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('trains/create/', views.add_train, name='add_train'),
    path('trains/availability/', views.check_availability, name='check_availability'),
    path('trains/<int:train_id>/book/', views.book_seat, name='book_seat'),
]
