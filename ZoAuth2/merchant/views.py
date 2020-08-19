from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse, resolve, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .forms import NewUserForm, CreateProductForm
from .models import Product
import datetime
# Create your views here.

@csrf_exempt
def create_product(request):
    product = Product(
        name=request.POST.get('name'),
        address=request.POST.get('address'),
        period=datetime.timedelta(int(request.POST.get('period'))),
        scope=request.POST.get('scope'),
        price=int(request.POST.get('price')),
    )
    product.save()
    return JsonResponse({'product': product.name})

def get_products(request):
    products = Product.objects.all()
    return JsonResponse([{
        'address': product.address,
        'price': product.price,
        'scope': product.scope} for product in products], safe=False)

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("/merchant/dashboard")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: form.error_messages[msg]")

                return render(
                    request=request,
                    template_name="register.html",
                    context={"form": form}
                )

    form = NewUserForm
    return render(
        request=request,
        template_name="register.html",
        context={"form": form}
    )

def logout_request(request):
    logout(request)
    messages.info(request, "Logged Out Successfully!")
    return redirect("merchant:login")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(
            request=request,
            data=request.POST
        )
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('merchant:dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request,
        template_name="login.html",
        context={"form": form}
    )

class DashboardView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('merchant:login')
    model = Product
    template_name = 'dashboard.html'

class CreateProductView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('merchant:login')
    model = Product
    template_name = 'create_product.html'
    success_url = reverse_lazy('merchant:dashboard')
    form_class = CreateProductForm
    #Form needs to validate
    # Valid zaddress based on chain parameter
    # form needs to take dropdown input for period and convert it to datetime.duration
    # two workflows for assigning an oauth_scope to external resources and assigning a category or content view for local resources
