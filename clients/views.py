from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from clients.models import Client, Registration, Transaction, TransactionSettings
from calendarapp.models import Event
from calendarapp.models.event import Package, PackageType
from clients.forms import ClientForm, RegistrationStep1Form, RegistrationStep2Form, TransactionForm, TransactionSettingsForm
from django.views.decorators.csrf import csrf_exempt
import json

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
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Client added successfully'
            })
        else:
            errors = {field: form.errors.get(field) for field in form.fields}
            return JsonResponse({
                'success': False,
                'errors': errors
            })

    return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

@login_required(login_url="signup")
def get_registrations(request):
    registrations_list = Registration.objects.all()
    context = {"registrations_list":registrations_list}
    return render(request, 'registrations.html', context)

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
                'payment_method': form.cleaned_data['payment_method'],  # String
            }
            request.session['step1_data'] = step1_data
            return redirect('clientsapp:registration_step2')  # Redirect to Step 2
    else:
        form = RegistrationStep1Form()
    return render(request, 'registration_step1.html', {'form': form})

@login_required(login_url="signup")
def registration_step2(request):
    step1_data = request.session.get('step1_data')
    if not step1_data:
        return redirect('clientsapp:registration_step1')  # Redirect back to Step 1 if no session data

    package = get_object_or_404(Package, id=step1_data['package'])
    package_price = package.get_price(Client.objects.get(id=step1_data['client']).is_member)

    if request.method == 'POST':
        form = RegistrationStep2Form(request.POST)
        if form.is_valid():
            price_paid = form.cleaned_data['price_paid']

            # Create the registration object using stored IDs
            Registration.objects.create(
                client=Client.objects.get(id=step1_data['client']),
                class_obj=Event.objects.get(id=step1_data['class_obj']),
                package_type=PackageType.objects.get(id=step1_data['package_type']),
                package=package,
                payment_type=step1_data['payment_type'],
                payment_method=step1_data['payment_method'],
                price_paid=price_paid,
            )
            return redirect('clientsapp:registrations')  # Redirect to the list of registrations
    else:
        form = RegistrationStep2Form()

    return render(request, 'registration_step2.html', {'form': form, 'package_price': package_price})

@login_required(login_url="signup")
def get_packages(request):
    package_type_id = request.GET.get('package_type_id')
    if package_type_id :
        packages = Package.objects.filter(package_type_id=package_type_id)
        data = [{'id': pkg.id, 'name': str(pkg)} for pkg in packages]
        return JsonResponse({'packages': data}, safe=False)
    return JsonResponse({'error': 'Invalid Package Type ID'}, status=400)

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
                if attended:
                    try:
                        registration = Registration.objects.get(id=member_id)
                        if registration.classes_left > 0:
                            registration.classes_left -= 1
                            registration.classes_attended += 1
                            registration._force_manual_update = True
                            registration.save()
                            print(f"Updated Registration: {registration.client.name}, "
                                  f"Classes Left: {registration.classes_left}, "
                                  f"Classes Attended: {registration.classes_attended}")
                        else:
                            print(f"Registration {member_id} has no classes left.")
                    except Registration.DoesNotExist:
                        print(f"Registration with ID {member_id} not found.")
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required(login_url="signup")
def get_transactions(request):
    transactions_list = Transaction.objects.all()
    context = {"transactions_list":transactions_list}
    return render(request, 'transactions.html', context)

@login_required
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
