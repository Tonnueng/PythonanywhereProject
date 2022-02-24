from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages




# Create your views here.
from .forms import CreateUserForm
from .models import Category, Photo

def home(request):
    return render(request,'home/home.html')
    #return HttpResponse('<h1>HelloWorld</h1>')

def gallery(request):
    category = request.GET.get('category')

    if category == None:
        photos = Photo.objects.all
    else:
        photos = Photo.objects.filter(category__name=category)

    categories = Category.objects.all

    context = {'categories': categories, 'photos': photos}
    return render(request, 'home/gallery.html', context)

def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request,'home/photo.html',{'photo': photo})

def addPhoto(request):
    if request.user.is_authenticated:
        pass
    else:
        messages.error(request, 'โปรดเข้าสู่ระบบ')
        return redirect('login')
    categories = Category.objects.all()
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,)

        return redirect('gallery')

    context ={'categories':categories}
    return render(request,'home/add.html', context)

def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('login')
    else:
        form = CreateUserForm()

    return render(request, 'home/register.html', {'form': form})



def loginpage(request):
    if request.user.is_authenticated:
       return redirect('home-page')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home-page')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'home/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def noomlamoon(request):
    return render(request,'home/noomlamoon.html')

def shadecafe(request):
    return render(request,'home/Shadecafe.html')

def fongnomcafe(request):
    return render(request,'home/fongnom.html')

























