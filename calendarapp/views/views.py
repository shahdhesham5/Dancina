from django.shortcuts import render, redirect,  get_object_or_404
from django.http import JsonResponse
from itertools import groupby
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from calendarapp.forms import AddInstructorForm , AddStudioForm
from calendarapp.models.event import Instructor, StudioLocation, Package, PackageType
from django.contrib import messages
from accounts.decorators import allowed_users

@login_required(login_url="signup")
def get_instructors(request):
    instructors_list = Instructor.objects.all()
    context = {"instructors_list":instructors_list}
    return render(request, 'instructors.html', context)

@login_required(login_url="signup")
def add_instructor(request):
    if request.method == 'POST':
        form = AddInstructorForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Instructor added successfully'
            })
        else:
            errors = {field: form.errors.get(field) for field in form.fields}
            return JsonResponse({
                'success': False,
                'errors': errors
            })

    return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

@allowed_users(groups=['Dancina SuperAdmin'])
def delete_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    
    if request.method == 'POST':
        instructor.delete()
        messages.success(request, 'Instructor deleted successfully.')
        return redirect('calendarapp:instructors')

@allowed_users(groups=['Dancina SuperAdmin'])
def edit_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)

    if request.method == 'POST':
        form = AddInstructorForm(request.POST, instance=instructor) 
        if form.is_valid():
            form.save()
            return redirect('calendarapp:instructors')
    else:
        form = AddInstructorForm(instance=instructor)

    return render(request, 'edit_instructor.html', {'form': form, 'instructor': instructor})


@login_required(login_url="signup")
def get_studios(request):
    studios_list = StudioLocation.objects.all()
    context = {"studios_list":studios_list}
    return render(request, 'studios.html', context)

@login_required(login_url="signup")
def add_studio(request):
    if request.method == 'POST':
        form = AddStudioForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Studio added successfully'
            })
        else:
            errors = {field: form.errors.get(field) for field in form.fields}
            return JsonResponse({
                'success': False,
                'errors': errors
            })

    # Render empty form on GET request
    form = AddStudioForm()
    return render(request, 'studios.html', {'form': form})

@allowed_users(groups=['Dancina SuperAdmin'])
def delete_studio(request, studio_id):
    studio = get_object_or_404(StudioLocation, pk=studio_id)
    
    if request.method == 'POST':
        studio.delete()
        messages.success(request, 'Studio deleted successfully.')
        return redirect('calendarapp:studios')

@allowed_users(groups=['Dancina SuperAdmin'])
def edit_studio(request, studio_id):
    studio = get_object_or_404(StudioLocation, pk=studio_id)

    if request.method == 'POST':
        form = AddStudioForm(request.POST, instance=studio) 
        if form.is_valid():
            form.save()
            return redirect('calendarapp:studios')
    else:
        form = AddStudioForm(instance=studio)

    return render(request, 'edit_studio.html', {'form': form, 'studio': studio})


@login_required(login_url="signup")
def get_packages(request):
    # Fetch packages and order by package_type to prepare for groupby
    packages_list = Package.objects.select_related('package_type').order_by('package_type')

    # Group packages by package_type
    grouped_packages = groupby(packages_list, key=lambda x: x.package_type)

    # Convert the groupby result into a list of tuples (package_type, list of packages)
    grouped_packages = [(package_type, list(packages)) for package_type, packages in grouped_packages]
    package_types = PackageType.objects.all()
    context = {"grouped_packages": grouped_packages, "package_types":package_types}
    return render(request, 'packages.html', context)

@csrf_exempt
@login_required(login_url="signup")
def add_package(request):
    if request.method == 'POST':
        try:
            # Get the package type data
            package_type_id = request.POST.get('package_type')
            new_package_type_name = request.POST.get('new_package_type')

            # Check if a new package type was provided
            if new_package_type_name:
                package_type, created = PackageType.objects.get_or_create(name=new_package_type_name)
            else:
                package_type = PackageType.objects.get(id=package_type_id)

            # Create and save the new package
            package = Package(
                package_type=package_type,
                number_of_sessions=request.POST['number_of_sessions'],
                member_price=request.POST['member_price'],
                non_member_price=request.POST['non_member_price'],
                
                member_price_per_class=request.POST['member_price_per_class'],
                non_member_price_per_class=request.POST['non_member_price_per_class'],
                duration=int(request.POST['duration'])   # Use the duration_months value
            )
            package.save()

            # Return a successful JSON response
            return JsonResponse({'success': True})

        except Exception as e:
            # Return an error JSON response with details
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

@allowed_users(groups=['Dancina SuperAdmin'])
def delete_package_type(request, package_type_id):
    package_type = get_object_or_404(PackageType, pk=package_type_id)
    
    if request.method == 'POST':
        package_type.delete()
        messages.success(request, 'Package Type deleted successfully.')
        return redirect('calendarapp:packages')

@allowed_users(groups=['Dancina SuperAdmin'])
def delete_package(request, package_id):
    package = get_object_or_404(Package, pk=package_id)
    
    if request.method == 'POST':
        package.delete()
        messages.success(request, 'Package deleted successfully.')
        return redirect('calendarapp:packages')

