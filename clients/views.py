from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from clients.models import Client, Registration
from calendarapp.models import Event
from calendarapp.models.event import Package, PackageType
from clients.forms import ClientForm, RegistrationStep1Form, RegistrationStep2Form

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

