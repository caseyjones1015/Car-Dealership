from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import CarBrand, CarModel, Car, CarImage, AdditionalCarImage, FinancialDetails, LegalDocument
from django.contrib import messages
from users.models import Role
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, user_required
from django.contrib.auth import get_user_model


# Create your views here.
def main(request):
    return render(request, 'main.html')


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


def custom_500_view(request):
    return render(request, '500.html', status=500)


@user_required
def car_dealership_view(request, model_name=None, brand_name=None):
    car_brands = CarBrand.objects.all()
    cars = Car.objects.filter(available=True)
    car_model = None
    car_brand = None

    if brand_name:
        car_brand = get_object_or_404(CarBrand, name=brand_name)

    if model_name:
        car_model = get_object_or_404(CarModel, name=model_name)
        cars = Car.objects.filter(car_model=car_model)

    context = {
        'car_brands': car_brands,
        'car_model': car_model,
        'car_brand': car_brand,
        'cars': cars,
    }

    return render(request, 'main.html', context)


@admin_required
def sales_stats(request):
    sold_cars = Car.objects.filter(available=False)
    car_brands = CarBrand.objects.all()

    context = {
        'sold_cars': sold_cars,
        'car_brands': car_brands,
    }
    return render(request, 'admin/sales_stats.html', context)


@user_required
def car_details(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    financial_details, created = FinancialDetails.objects.get_or_create(car=car)

    # Retrieve all car brands for the sidebar
    car_brands = CarBrand.objects.all()

    context = {
        'car': car,
        'car_brands': car_brands,
        'financial_details': financial_details,
    }

    return render(request, 'car_details.html', context)


@admin_required
def admin_home(request):
    users_with_roles = User.objects.prefetch_related('role').all()
    context = {
        'users_with_roles': users_with_roles
    }

    return render(request, 'admin/admin_home.html', context)


@admin_required
def brand_list(request):
    car_brands = CarBrand.objects.all()

    context = {
        'car_brands': car_brands
    }

    return render(request, 'admin/brand_list.html', context)


@admin_required
def model_list(request):
    car_models = CarModel.objects.all()
    car_brands = CarBrand.objects.all()

    context = {
        'car_models': car_models,
        'car_brands': car_brands,
    }

    return render(request, 'admin/model_list.html', context)


@admin_required
def car_list(request):
    car = Car.objects.all()

    context = {
        'car': car
    }

    return render(request, 'admin/car_list.html', context)


@admin_required
def add_car_brand(request):
    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')
        if brand_name:
            CarBrand.objects.create(name=brand_name)
            return redirect('brand_list')
        else:
            messages.error(request, 'Brand name cannot be empty.')

    return render(request, 'admin/add_car_brand.html')


@admin_required
def add_car_model(request):
    if request.method == 'POST':
        brand_id = request.POST.get('car_brand')
        model_name = request.POST.get('model_name')

        if brand_id and model_name:
            car_brand = CarBrand.objects.get(id=brand_id)
            CarModel.objects.create(name=model_name, brand=car_brand)
            return redirect('model_list')
        else:
            messages.error(request, 'Brand and model name are required.')

    car_brands = CarBrand.objects.all()
    context = {
        'car_brands': car_brands,
    }

    return render(request, 'admin/add_car_model.html', context)


@admin_required
def add_car(request):
    if request.method == 'POST':
        model_id = request.POST.get('car')
        year = request.POST.get('year')
        price = request.POST.get('price')
        mileage = request.POST.get('kilo')
        grade = request.POST.get('grade')
        color = request.POST.get('color')
        optional = request.POST.get('optional')
        available = request.POST.get('available')
        available_status = available == 'true' if available is not None else False

        if not grade:
            grade = 'N/A'
        if not color:
            color = 'N/A'

        if model_id and year and price and mileage:
            car_model = CarModel.objects.get(id=model_id)
            new_car, created = Car.objects.get_or_create(
                car_model=car_model,
                year=year,
                price=price,
                mileage=mileage,
                grade=grade,
                color=color,
                optional=optional,
                available=bool(available),
            )

            car_images = request.FILES.getlist('car_images')
            for image in car_images:
                car_image_instance = CarImage.objects.create(car=new_car, image=image)

            additional_car_images = request.FILES.getlist('additional_images')
            for additional_image in additional_car_images:
                AdditionalCarImage.objects.create(car=new_car, additional_image=additional_image)

            # Set the first uploaded image as the default image for the carousel
            if car_images:
                new_car.default_image = car_images[0]
                new_car.save()

            return redirect('car_list')
        else:
            messages.error(request, 'Please fill in all required fields.')

    car_models = CarModel.objects.all()
    context = {
        'car_models': car_models,
    }

    return render(request, 'admin/add_car.html', context)


@admin_required
def edit_brand(request, brand_id):
    brand = get_object_or_404(CarBrand, id=brand_id)

    if request.method == 'POST':
        new_name = request.POST.get('brand_name')
        if new_name:
            brand.name = new_name
            brand.save()
            return redirect('brand_list')
        else:
            messages.error(request, 'Brand name cannot be empty.')
            # Pass the existing brand object back to the form for correction
            return render(request, 'admin/add_car_brand.html', {'brand': brand})

    context = {
        'brand': brand,
    }
    return render(request, 'admin/add_car_brand.html', context)


@admin_required
def delete_brand(request, brand_id):
    brand = get_object_or_404(CarBrand, id=brand_id)

    if request.method == 'POST':
        brand.delete()
        return redirect('brand_list')

    context = {
        'brand': brand,
    }
    return render(request, 'admin/add_car_brand.html', context)


@admin_required
def edit_model(request, model_id):
    car_model = get_object_or_404(CarModel, id=model_id)
    car_brand = car_model.brand
    car_brands = CarBrand.objects.all()

    if request.method == 'POST':
        new_name = request.POST.get('model_name')
        if new_name:
            car_model.name = new_name
            car_model.save()
            return redirect('model_list')
        else:
            messages.error(request, 'Model name cannot be empty.')
            # Pass the existing model object back to the form for correction
            return render(request, 'admin/add_car_model.html', {'car_model': car_model})

    context = {
        'car_model': car_model,
        'car_brand': car_brand,
        'car_brands': car_brands,
    }
    return render(request, 'admin/add_car_model.html', context)


@admin_required
def delete_model(request, model_id):
    car_model = get_object_or_404(CarModel, id=model_id)

    if request.method == 'POST':
        car_model.delete()
        return redirect('model_list')

    context = {
        'car_model': car_model,
    }
    return render(request, 'admin/add_car_model.html', context)


@admin_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        car.delete()
        return redirect('car_list')

    context = {
        'car': car,
    }
    return render(request, 'admin/add_car.html', context)


@admin_required
def delete_selected_brands(request):
    if request.method == 'POST':
        selected_brand_ids = request.POST.getlist('selected_brands[]')
        if selected_brand_ids:
            brands_to_delete = CarBrand.objects.filter(id__in=selected_brand_ids)
            brands_to_delete.delete()
            messages.success(request, 'Selected brands deleted successfully.')
        else:
            messages.error(request, "No brands selected for deletion.")
    return redirect('brand_list')


@admin_required
def delete_selected_models(request):
    if request.method == 'POST':
        selected_model_ids = request.POST.getlist('selected_models[]')
        if selected_model_ids:
            models_to_delete = CarModel.objects.filter(id__in=selected_model_ids)
            models_to_delete.delete()
            messages.success(request, 'Selected models deleted successfully.')
        else:
            messages.error(request, "No models selected for deletion.")
    return redirect('model_list')


@admin_required
def delete_selected_cars(request):
    if request.method == 'POST':
        selected_car_ids = request.POST.getlist('selected_cars[]')
        if selected_car_ids:
            cars_to_delete = Car.objects.filter(id__in=selected_car_ids)
            cars_to_delete.delete()
            messages.success(request, 'Selected cars deleted successfully.')
        else:
            messages.error(request, "No cars selected for deletion.")
    return redirect('car_list')


@admin_required
def delete_selected_users(request):
    if request.method == 'POST':
        selected_user_ids = request.POST.getlist('selected_users[]')
        if selected_user_ids:
            users_to_delete = User.objects.filter(id__in=selected_user_ids)
            users_to_delete.delete()
            messages.success(request, 'Selected users deleted successfully.')
        else:
            messages.error(request, "No users selected for deletion.")
    return redirect('admin_home')


@admin_required
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car_model = car.car_model
    car_models = CarModel.objects.all()

    if request.method == 'POST':
        year = request.POST.get('year')
        price = request.POST.get('price')
        mileage = request.POST.get('kilo')
        grade = request.POST.get('grade')
        color = request.POST.get('color')
        optional = request.POST.get('optional')
        seater = request.POST.get('seater')
        available = request.POST.get('available') == 'on'

        if not grade:
            grade = 'N/A'
        if not color:
            color = 'N/A'

        if year and price and mileage:
            car.year = year
            car.price = price
            car.mileage = mileage
            car.grade = grade
            car.color = color
            car.seater = seater
            car.optional = optional
            car.available = available
            car.save()

            # Handle image update if needed
            car_image = request.FILES.get('car_image')
            if car_image:
                car.image = car_image
                car.save()

            messages.success(request, 'Car details updated successfully.')
            return redirect('car_list')
        else:
            messages.error(request, 'Please fill in all required fields.')
            # Pass the existing car object back to the form for correction
            context = {
                'car': car,
            }
            return render(request, 'admin/add_car.html', context)

    context = {
        'car': car,
        'car_model': car_model,
        'car_models': car_models,
        'optional': car.optional,
    }
    return render(request, 'admin/add_car.html', context)


@admin_required
def add_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Set default role for the user
            default_role = Role(role=Role.GUEST, user=user)
            default_role.save()

            messages.success(request, "User created successfully!")
            return redirect('admin_home')  # Redirect after successful user creation
        else:
            messages.error(request, "There was an error with your form")
    else:
        form = UserCreationForm()  # Render an empty form for GET requests

    return render(request, 'admin/add_user.html', {'form': form})


@admin_required
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    form = PasswordChangeForm(user)  # Initialize form outside conditional blocks
    roles = Role.ROLE_CHOICES

    if request.method == "POST":
        # Logic for changing username
        if 'change_username' in request.POST:
            new_username = request.POST.get('new_username')
            if new_username:
                user.username = new_username
                user.save()
                messages.success(request, "Username updated successfully!")
                return redirect('admin_home')

        # Logic for changing password
        elif 'change_password' in request.POST:
            if request.user.role.role == 'admin':  # Superuser changing password without old password
                form = SetPasswordForm(user, request.POST)
            else:  # Non-superuser changing password with old password
                form = PasswordChangeForm(user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "Password updated successfully!")
                return redirect('admin_home')
            else:
                messages.error(request, "There was an error with your form")

        elif 'change_roles' in request.POST:
            selected_role = request.POST.get('new_role')
            if selected_role:  
                user_role, created = Role.objects.get_or_create(user=user)
                user_role.role = selected_role
                user_role.save()
                messages.success(request, "Roles updated successfully!")
                return redirect('admin_home')

    else:
        if request.user.role.role == 'admin':  # Initialize forms based on user status
            form = SetPasswordForm(user)
        else:
            form = PasswordChangeForm(user)

    context = {
        'user': user,
        'form': form,
        'roles': roles,
    }

    return render(request, 'admin/edit_user.html', context)


@admin_required
def delete_user(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        user.delete()
        # Optionally, add a success message
        messages.success(request, "User deleted successfully!")
        return redirect('admin_home')  # Redirect to admin home or any other page

    context = {
        'user': user,
    }

    return render(request, 'admin/add_user.html', context)


@admin_required
def additional_images(request, car_id):
    car_images = AdditionalCarImage.objects.filter(car_id=car_id)

    context = {
        'car_images': car_images
    }

    return render(request, 'additional_images.html', context)


@admin_required
def save_financial_details(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    financial_details, created = FinancialDetails.objects.get_or_create(car=car)

    if request.method == 'POST':
        financial_details.buy_co = request.POST.get('buy_co', financial_details.buy_co)
        financial_details.buy_amount = request.POST.get('buy_amount', financial_details.buy_amount)
        financial_details.buy_additional = request.POST.get('buy_additional', financial_details.buy_additional)
        financial_details.buy_total = request.POST.get('buy_total', financial_details.buy_total)

        financial_details.repair_co = request.POST.get('repair_co', financial_details.repair_co)
        financial_details.repair_amount = request.POST.get('repair_amount', financial_details.repair_amount)
        financial_details.repair_additional = request.POST.get('repair_additional', financial_details.repair_additional)
        financial_details.repair_total = request.POST.get('repair_total', financial_details.repair_total)

        financial_details.sold_co = request.POST.get('sold_co', financial_details.sold_co)
        financial_details.sold_amount = request.POST.get('sold_amount', financial_details.sold_amount)
        financial_details.sold_additional = request.POST.get('sold_additional', financial_details.sold_additional)
        financial_details.sold_total = request.POST.get('sold_total', financial_details.sold_total)

        financial_details.brokage_co = request.POST.get('brokage_co', financial_details.brokage_co)
        financial_details.brokage_amount = request.POST.get('brokage_amount', financial_details.brokage_amount)
        financial_details.brokage_additional = request.POST.get('brokage_additional', financial_details.brokage_additional)
        financial_details.brokage_total = request.POST.get('brokage_total', financial_details.brokage_total)

        financial_details.profit = request.POST.get('profit', financial_details.profit)
        financial_details.note = request.POST.get('note', financial_details.note)

        financial_details.save()

        return redirect('car_details', car_id=car.id)

    context = {
        'car': car,
        'financial_details': financial_details,
    }

    return render(request, 'car_details.html', context)


@admin_required
def upload_legal_documents(request, car_id):
    if request.method == 'POST' and request.FILES.getlist('legal_documents'):
        car = Car.objects.get(id=car_id)
        legal_documents = request.FILES.getlist('legal_documents')

        for document in legal_documents:
            legal_doc = LegalDocument(car=car, legal_document=document)
            legal_doc.save()

            financial_details, created = FinancialDetails.objects.get_or_create(car=car)
            financial_details.legal_documents.add(legal_doc)

        return redirect('car_details', car_id=car.id)
    else:
        return JsonResponse({'status': 'error', 'message': 'Failed to upload legal documents.'})


@admin_required
def display_legal_documents(request, car_id):
    financial_details = FinancialDetails.objects.filter(car_id=car_id)
    legal_documents = []

    for details in financial_details:
        documents = details.legal_documents.all()
        legal_documents.extend(documents)

    context = {
        'legal_documents': legal_documents,
    }

    return render(request, 'legal_documents.html', context)


@admin_required
def clear_legal_documents(request, car_id):
    financial_details = FinancialDetails.objects.filter(car_id=car_id).first()
    if financial_details:
        financial_details.legal_documents.clear()

    return redirect(request, 'car_details', car_id=car_id)


@admin_required
def cancel_brand(request):
    return redirect('brand_list')


@admin_required
def cancel_model(request):
    return redirect('model_list')


@admin_required
def cancel_car(request):
    return redirect('car_list')


@admin_required
def cancel_user(request):
    return redirect('admin_home')


def test(request):
    return render(request, 'test.html')


def test2(request):
    return render(request, '404.html')