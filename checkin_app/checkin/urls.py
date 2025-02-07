from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_login, name='redirect_to_login'),
    path('checkin/', views.workplace_list, name='workplace_list'),
    path('checkin/<int:workplace_id>/', views.checkin_checkout, name='checkin_checkout'),
    path('report/<int:user_id>/', views.weekly_report, name='weekly_report'),
    path('add_workplace/', views.add_workplace, name='add_workplace'),
]