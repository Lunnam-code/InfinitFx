from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('signout/', views.signout, name='signout'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('reset_passwordvalidate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    
    # dashboard 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('deposite/', views.deposite, name='deposite'),
    path('invest/', views.invest, name='invest'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('investment/', views.investment, name='investment'),
    path('profile/', views.profile, name='profile'),
    path('setting/', views.setting, name='setting'),
    path('profileImage/', views.profileImage, name='profileImage'),
    path('referralfun/', views.referralfun, name='referral'),
    path('deposit_list/', views.deposit_list, name='deposit_list'),
    path('account_history/', views.account_history, name='account_history'),
]
