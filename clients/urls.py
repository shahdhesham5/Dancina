from django.urls import path
from . import views
app_name = "clientsapp"


urlpatterns = [
    path("clients/",views.get_clients,name="clients"),
    path('add-client/', views.add_client, name='add_client'),
    path('edit-client/<int:pk>/',views.edit_client, name="edit-client"),
    path('delete-client/<int:pk>/',views.delete_client, name="delete-client"),

    path('registrations/',views.get_registrations,name='registrations'),
    path('delete-registration/<int:pk>/',views.delete_registration, name="delete-registration"),
    path('registrations/step1/', views.registration_step1, name='registration_step1'),
    path('registrations/step2/', views.registration_step2, name='registration_step2'),
    
    path('get-packages/', views.get_packages, name="get-packages"),
    path('attendance/', views.save_attendance, name="save_attendance"),
    path('get-attendances/', views.get_attendances, name="attendance"),
    path('delete-attendance/<int:pk>/', views.delete_attendance, name="delete_attendance"),
    
    path('transaction-settings/',views.update_transaction_settings,name='transaction_settings'),
    path('transactions/',views.get_transactions,name='transactions'),
    path('delete-transaction/<int:pk>/',views.delete_transaction,name='delete_transaction'),
    path('add-transaction/',views.add_transaction,name='add_transaction'),
    path('get-payment-methods/', views.get_payment_methods, name='get_payment_methods'),       
    path('get_clients/',views.get_clients_for_transactionForm,name='get_clients'),
    
]