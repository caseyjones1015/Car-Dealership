from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('car_dealership')
        else:
            messages.error(request, ("There Was An Error Logging In, Try Again..."))
            return redirect('user_login')
    else:
        return render(request, 'authenticate/login.html')


def user_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Successful!")
            return redirect('user_login')  # Redirect to login after successful registration
        else:
            messages.error(request, ("There Was An Error With Your Form!"))
    else:
        form = UserCreationForm()  # Render an empty form for GET requests

    return render(request, 'authenticate/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return redirect('user_login')
