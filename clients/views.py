from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from clients.models import Client, Registration, Transaction, TransactionSettings, Attendance
from calendarapp.models import Event
from calendarapp.models.event import Package, PackageType, ClassOccurrence
from clients.forms import ClientForm, RegistrationStep1Form, RegistrationStep2Form, TransactionForm, TransactionSettingsForm
from django.views.decorators.csrf import csrf_exempt
import json
from accounts.decorators import allowed_users
from django.utils.timezone import now
from django.contrib import messages
import logging
logger = logging.getLogger(__name__)


# Clients
@login_required(login_url="signup")
def get_clients(request):
    clients_list = Client.objects.all()
    context = {"clients_list":clients_list}
    return render(request, 'clients.html', context)

@login_required(login_url="signup")
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            # form.save()
            return JsonResponse({
                'success': True,
                'client_id': client.id  
            })
        else:
            errors = {field: form.errors.get(field) for field in form.fields}
            return JsonResponse({
                'success': False,
                'errors': errors
            })

    return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

@login_required(login_url="signup")
@allowed_users(groups=['Dancina SuperAdmin'])
def edit_client(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client) 
        if form.is_valid():
            form.save()
            return redirect('clientsapp:clients')
    else:
        form = ClientForm(instance=client)

    return render(request, 'edit_client.html', {'form': form, 'client': client})

@login_required(login_url="signup")
@allowed_users(groups=['Dancina SuperAdmin'])
def delete_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Client deleted successfully.')
        return redirect('clientsapp:clients')



# Registrations
@login_required(login_url="signup")
def get_registrations(request):
    registrations_list = Registration.objects.all()

    # Convert expiration_date to date for comparison
    for regist in registrations_list:
        if hasattr(regist, 'expiration_date') and regist.expiration_date:
            regist.expiration_date = regist.expiration_date.date()
        else:
            regist.expiration_date_minus_one_week = None
            
        # Calculate half of the number of sessions in the package
        if hasattr(regist.package, 'number_of_sessions') and regist.package.number_of_sessions:
            regist.half_sessions = regist.package.number_of_sessions / 2
        else:
            regist.half_sessions = 0
    today = now().date()
    context = {"registrations_list": registrations_list, "today": today}
    return render(request, 'registrations.html', context)

@login_required(login_url="signup")
@allowed_users(groups=['Dancina SuperAdmin'])
def delete_registration(request, pk):
    regist = get_object_or_404(Registration, pk=pk)
    if request.method == 'POST':
        regist.delete()
        messages.success(request, 'Registration deleted successfully.')
        return redirect('clientsapp:registrations')

@login_required(login_url="signup")
def registration_step1(request):
    if request.method == 'POST':
        form = RegistrationStep1Form(request.POST)
        if form.is_valid():
            # Serialize the cleaned data to store in session
            step1_data = {
                'client': form.cleaned_data['client'].id,  # Store client ID
                'class_obj': form.cleaned_data['class_obj'].id,  # Store class ID
                'package_type': form.cleaned_data['package_type'].id,  # Store package type ID
                'package': form.cleaned_data['package'].id,  # Store package ID
                'payment_type': form.cleaned_data['payment_type'],  # String
            }
            request.session['step1_data'] = step1_data
            return redirect('clientsapp:registration_step2')  
    else:
        client_id = request.GET.get('client_id')
        form = RegistrationStep1Form(initial={'client': client_id})  # Prepopulate the form with the client ID
    return render(request, 'registration_step1.html', {'form': form})

@login_required(login_url="signup")
def registration_step2(request):
    step1_data = request.session.get('step1_data')
    if not step1_data:
        return redirect('clientsapp:registration_step1') 

    package = get_object_or_404(Package, id=step1_data['package'])
    package_price = package.get_price(Client.objects.get(id=step1_data['client']).is_member)
   

    if request.method == 'POST':
        form = RegistrationStep2Form(request.POST)
        if form.is_valid():
            price_paid = form.cleaned_data['price_paid']
            payment_method = form.cleaned_data['payment_method']

            # Create the registration object using stored IDs
            registration = Registration.objects.create(
                client=Client.objects.get(id=step1_data['client']),
                class_obj=Event.objects.get(id=step1_data['class_obj']),
                package_type=PackageType.objects.get(id=step1_data['package_type']),
                package=package,
                payment_type=step1_data['payment_type'],
                price_paid=price_paid,
            )
            Transaction.objects.create(
                client=registration.client,
                registration=registration,
                value_paid=price_paid,
                payment_method=payment_method,
                date=now(),
            )
            if registration.class_obj.is_private:
                Attendance.objects.create(
                    client=registration.client,
                    event=registration.class_obj,
                    attendance_date=registration.registration_date
                )
                # Update the registration attendance details
                registration.classes_attended += 1
                registration.classes_left = max(0, registration.classes_left - 1)
                registration.save()
                
            return redirect('clientsapp:registrations') 
    else:
        form = RegistrationStep2Form()

    return render(request, 'registration_step2.html', {'form': form, 'package_price': package_price})



# Packages
@login_required(login_url="signup")
def get_packages(request):
    package_type_id = request.GET.get('package_type_id')
    if package_type_id :
        packages = Package.objects.filter(package_type_id=package_type_id)
        data = [{'id': pkg.id, 'name': str(pkg)} for pkg in packages]
        return JsonResponse({'packages': data}, safe=False)
    return JsonResponse({'error': 'Invalid Package Type ID'}, status=400)


# Attendance
@login_required(login_url="signup")
def get_attendances(request):
    attendances_list = Attendance.objects.all()
    context = {"attendances_list":attendances_list}
    return render(request, 'attendance.html', context)

@csrf_exempt
@login_required(login_url="signup")
def save_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            attendance = data.get('attendance', [])

            for record in attendance:
                member_id = record.get('memberId')
                attended = record.get('attended')
                ClassOccurrence_id = record.get('class_occurrence_id')

                # Log to debug if we are receiving the correct attendance data
                print(f"Attendance record: memberId={member_id}, attended={attended}")

                if attended:
                    try:
                        registration = Registration.objects.get(id=member_id)
                        class_occurrence = ClassOccurrence.objects.get(id=ClassOccurrence_id)
                
                        if registration.classes_left > 0:
                            registration.classes_left -= 1
                            registration.classes_attended += 1
                            registration._force_manual_update = True
                            registration.save()

                            # Create the attendance record with the correct occurrence date
                            Attendance.objects.create(
                                client=registration.client,
                                event=registration.class_obj,
                                attendance_date=class_occurrence.date,  # Set the attendance date to match the class occurrence
                            )
                            print(f"Attendance recorded for {registration.client.name} on {class_occurrence.date}")
                        else:
                            print(f"Registration {member_id} has no classes left.")
                    except Registration.DoesNotExist:
                        print(f"Registration with ID {member_id} not found.")
                    except ClassOccurrence.DoesNotExist:
                        print(f"ClassOccurrence with ID {class_occurrence} not found.")
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required(login_url="signup")
@allowed_users(groups=['Dancina SuperAdmin'])
def delete_attendance(request, pk):
    attend = get_object_or_404(Attendance, pk=pk)
    
    if request.method == 'POST':
        registration = Registration.objects.filter(
            client=attend.client, 
            class_obj=attend.event
        ).first()

        # Delete the attendance record
        attend.delete()

        # Update the registration counts
        if registration:
            registration.classes_attended = max(0, registration.classes_attended - 1)
            registration.classes_left += 1
            registration.save()
        messages.success(request, 'Attendance deleted successfully.')
        return redirect('clientsapp:attendance')
    
# Transactions
@login_required(login_url="signup")
def get_transactions(request):
    transactions_list = Transaction.objects.all()
    context = {"transactions_list":transactions_list}
    return render(request, 'transactions.html', context)

@login_required(login_url="signup")
@allowed_users(groups=['Dancina SuperAdmin'])
def delete_transaction(request, pk):
    trans = get_object_or_404(Transaction, pk=pk)
    
    if request.method == 'POST':
        trans.delete()
        messages.success(request, 'Transaction deleted successfully.')
        return redirect('clientsapp:transactions')

@login_required
@allowed_users(groups=['Dancina SuperAdmin'])
def update_transaction_settings(request):
    settings = TransactionSettings.objects.first()
    if not settings:
        settings = TransactionSettings.objects.create(starting_receipt_number=1)

    if request.method == 'POST':
        form = TransactionSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect("calendarapp:calendar")
    else:
        form = TransactionSettingsForm(instance=settings)

    return render(request, 'settings.html', {'form': form})

@login_required(login_url="signup")
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        registration_id = request.POST.get('registration')
        if form.is_valid() and registration_id:
            transaction = form.save(commit=False)

            # Fetch the specific registration
            registration = Registration.objects.get(id=registration_id)
            transaction.client = registration.client  # Link the transaction to the client
            transaction.save()

            # Update price_paid and price_left for the selected registration
            registration.price_paid += transaction.value_paid
            registration.price_left -= transaction.value_paid
            registration.save(update_fields=['price_paid', 'price_left'])

            return JsonResponse({
                'success': True,
                'new_price_left': registration.price_left,
                'new_price_paid': registration.price_paid
            })
        else:
            errors = {field: form.errors.get(field) for field in form.fields}
            return JsonResponse({'success': False, 'errors': errors})

def get_payment_methods(request):
    try:
        payment_methods = [{'value': method[0], 'label': method[1]} for method in Transaction.PAYMENT_METHOD_CHOICES]
        return JsonResponse(payment_methods, safe=False)
    except AttributeError:
        return JsonResponse({'error': 'PAYMENT_METHODS is not defined'}, status=500)

@login_required(login_url="signup")
def get_clients_for_transactionForm(request):
    # Fetch all registrations where price_left > 0
    registrations = Registration.objects.filter(price_left__gt=0).select_related('client', 'class_obj')

    # Structure the data to include client, class, and price_left details
    clients_with_registrations = [
        {
            'client_id': reg.client.id,
            'registration_id': reg.id,
            'client_name': reg.client.name,
            'class_name': reg.class_obj.name,
            'price_left': reg.price_left
        }
        for reg in registrations
    ]

    return JsonResponse(clients_with_registrations, safe=False)