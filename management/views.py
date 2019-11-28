from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import MealForm, ItemForm, UserForm
from django.views.decorators.csrf import csrf_protect
from .models import Meal, Item

# Create your views here.


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                meals = Meal.objects.filter(user=request.user)
                return render(request, 'index.html', {'meals': meals})
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                meals = Meal.objects.filter(user=request.user)
                return render(request, 'index.html', {'meals': meals})
    context = {
        "form": form,
    }
    return render(request, 'register.html', context)

@login_required
@csrf_protect
def index(request):
    meals = Meal.objects.filter(user=request.user)
    item_results = Item.objects.all()
    query = request.GET.get("q")
    if query:
        meals = meals.filter(
            Q(meal__icontains=query)
        ).distinct()
        item_results = item_results.filter(
            Q(item_name__icontains=query)
        ).distinct()
        return render(request, 'index.html', {
            'meals': meals,
            'items': item_results,
        })
    else:
        return render(request, 'index.html', {'meals': meals})


@login_required
@csrf_protect
def create_meal(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        form = MealForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            return render(request, 'detail.html', {'meal': meal})
        context = {
            "form": form,
        }
        return render(request, 'create_meal.html', context)


@login_required
@csrf_protect
def create_item(request, meal_id):
    form = ItemForm(request.POST or None, request.FILES or None)
    meal = get_object_or_404(Meal, pk=meal_id)
    if form.is_valid():
        meals_items = meal.item_set.all()
        for s in meals_items:
            if s.item_name == form.cleaned_data.get("item_name"):
                context = {
                    'meal': meal,
                    'form': form,
                    'error_message': 'You already added this meal',
                }
                return render(request, 'create_item.html', context)
        item = form.save(commit=False)
        item.meal = meal
        item.save()
        return render(request, 'detail.html', {'meal': meal})
    context = {
        'meal': meal,
        'form': form,
    }
    return render(request, 'create_item.html', context)


@login_required
@csrf_protect
def delete_item(request, meal_id, item_id):
    meal = get_object_or_404(Meal, pk=meal_id)
    item = Item.objects.get(pk=item_id)
    item.delete()
    return render(request, 'detail.html', {'meal': meal})


@login_required
@csrf_protect
def detail(request, meal_id):
    user = request.user
    meal = get_object_or_404(Meal, pk=meal_id)
    return render(request, 'detail.html', {'meal': meal, 'user': user})


@login_required
@csrf_protect
def delete_meal(request, meal_id):
    meal = Meal.objects.get(pk=meal_id)
    meal.delete()
    meals = Meal.objects.filter(user=request.user)
    return render(request, 'index.html', {'meals': meals})


@login_required
@csrf_protect
def update_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    form = MealForm(request.POST or None, request.FILES or None, instance=meal)
    if form.is_valid():
        meal = form.save(commit=False)
        meal.user = request.user
        meal.save()
        return render(request, 'detail.html', {'meal': meal})
    context = {
        "form": form,
    }
    return render(request, 'update_meal.html', context)


@login_required
@csrf_protect
def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'login.html', context)


@login_required
@csrf_protect
def items(request, filter_by):
    try:
        item_ids = []
        for meal in Meal.objects.filter(user=request.user):
            for item in meal.item_set.all():
                item_ids.append(item.pk)
        users_items = Item.objects.filter(pk__in=item_ids)
    except Meal.DoesNotExist:
        users_items = []
    return render(request, 'items.html', {
        'item_list': users_items,
        'filter_by': filter_by,
    })
