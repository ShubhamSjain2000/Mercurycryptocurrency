from django.urls import path
from . import views

urlpatterns = [

    path('',views.index,name = 'index'),
    path('register',views.register,name = 'register'),
    
    path('login',views.login,name = 'login'),
    path('transaction',views.transaction,name = 'transaction'),
    path('buycrypto',views.buycrypto,name = 'buycrypto'),
    path('logout',views.logout,name = 'logout'),
    path('get_balance',views.get_balance,name = 'get_balance'),
    
]