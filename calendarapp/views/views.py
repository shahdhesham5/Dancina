from django.shortcuts import render
from django.http import JsonResponse
from itertools import groupby
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from calendarapp.forms import AddInstructorForm , AddStudioForm, PackageForm
from calendarapp.models.event import Instructor, StudioLocation, Package, PackageType

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
    return render(request, 'your_template_path.html', {'form': form})


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
        package_type_id = request.POST.get('package_type')
        new_package_type_name = request.POST.get('new_package_type')

        # Check if a new package type was provided
        if new_package_type_name:
            package_type, created = PackageType.objects.get_or_create(name=new_package_type_name)
        else:
            package_type = PackageType.objects.get(id=package_type_id)

        package = Package(
            package_type=package_type,
            number_of_sessions=request.POST['number_of_sessions'],
            member_price=request.POST['member_price'],
            non_member_price=request.POST['non_member_price']
        )
        package.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})




# @csrf_exempt  # Make sure CSRF token is included in AJAX
# @login_required(login_url="signup")
# def add_package(request):
#     if request.method == 'POST':
#         form = PackageForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'success': False, 'errors': form.errors})
#     else:
#         form = PackageForm()
#     return render(request, 'packages.html', {'form': form})
