from django.urls import path
from . import views
app_name = "clientsapp"


urlpatterns = [
    path("clients/",views.get_clients,name="clients"),
    path('add-client/', views.add_client, name='add_client'),
    path('registrations/',views.get_registrations,name='registrations'),
    path('registrations/step1/', views.registration_step1, name='registration_step1'),
    path('registrations/step2/', views.registration_step2, name='registration_step2'),
    path('get-packages/', views.get_packages, name="get-packages"),
    path('attendance/', views.save_attendance, name="save_attendance"),
    path('transaction-settings/',views.update_transaction_settings,name='transaction_settings'),
    path('transactions/',views.get_transactions,name='transactions'),
    path('add-transaction/',views.add_transaction,name='add_transaction'),
    path('get_clients/',views.get_clients_for_transactionForm,name='get_clients'),
    
]