from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import User, images
from .forms import loginForm, userForm, imageForm



# Create your views here.

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def home(request):
    return render(request, 'images/home.html')

def userLogin(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            login(request, user)
            #return render(request, 'images/upload.html', {'image_form': image_form})
            return redirect('images:imageupload')
        else:
            messages.error(request, 'User Name or Password is incorrect')
            return render(request, 'images/login.html')
    else:
        form = loginForm()
    return render(request, 'images/login.html', {'form': form})

def logout_view(request):
    logout(request)

def registration(request):

    if request.method == 'POST':
        user_form = userForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.Allowed_IP = get_client_ip(request)
            user.is_student = True
            user.save()
            return render(request, 'images/register_done.html')
    else:
        user_form = userForm()
    return render(request, 'images/registration.html', {'user_form': user_form})

def userProfile(request):
    return render(request, 'images/user_profile.html')

def imageUpload(request):
        user = get_object_or_404(User, id=request.user.id)
        if request.method == 'POST':
            image_form = imageForm(data=request.POST, files=request.FILES, instance=user)
            if image_form.is_valid():
                image_form.userID = user
                image_form.save()
                messages.success(request, 'Image saved successfully!')
                return render(request, 'images/home.html')
            else:
                messages.error(request, 'Please correct the error below.')
                return render(request, 'images/home.html')
        else:
            image_form = imageForm()
            return render(request, 'images/upload.html', {'image_form': image_form})

def uploadedImages(request):
    all_images = images.objects.all()
    print (all_images)
    return redirect('images:imageupload')