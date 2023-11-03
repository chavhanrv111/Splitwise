from django.urls import path
from . import views

urlpatterns = [
    path('add_expense/', views.add_expense, name='add_expense'),
    path('view_balances/', views.view_balances, name='view_balances'),
    path('view_expenses/', views.view_expenses, name='view_expenses'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('home/', views.home, name='home'),
    path('passbook/', views.passbook, name='passbook'),
]