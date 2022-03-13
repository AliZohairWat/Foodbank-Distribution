from django.shortcuts import render, redirect
from .models import Category, Photo, Food
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
import datetime
# Create your views here.


def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('gallery')

    return render(request, 'photos/login_register.html', {'page': page})


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('gallery')

    context = {'form': form, 'page': page}
    return render(request, 'photos/login_register.html', context)


@login_required(login_url='login')
def gallery(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        foods = Food.objects.filter(category__user=user)
    else:
        foods = Food.objects.filter(
            category__name=category, category__user=user)

    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'foods': foods}
    return render(request, 'photos/gallery.html', context)


@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})

@login_required(login_url='login')
def viewFood(request, pk):
    food = Food.objects.get(id=pk)
    return render(request, 'foods/food.html', {'food': food})


@login_required(login_url='login')
def addPhoto(request):
    user = request.user

    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
            )

        return redirect('gallery')

@login_required(login_url='login')
def addFood(request):
    user = request.user

    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        # foodDict = [{'name': 'Chicken', 
        #               'weight': 5,
        #               'date': datetime.datetime(2020, 5, 17).date(),
        #               'glutenFree': True, 'halal': False},
        #              {'name': 'Beef', 
        #               'weight': 6,
        #               'date': datetime.datetime(2021, 2, 20).date(),
        #               'glutenFree': True, 'halal': False}, 
        #              {'name': 'Pork', 
        #               'weight': 8,
        #               'date': datetime.datetime(2016, 8, 18).date(),
        #               'glutenFree': True, 'halal': False}]

        # foodDict.append({'name': data, 
        #               'weight': 8,
        #               'date': datetime.datetime(2016, 8, 18).date(),
        #               'glutenFree': True, 'halal': False})


        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None
        
        
        food = Food.objects.create(
            category=category,
            name=data['name'],
            weight=data['weight'],
            date=data['date'],
            glutenFree=data['glutenFree'],
            halal=data['halal'],
        )

        # food.save()

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)
