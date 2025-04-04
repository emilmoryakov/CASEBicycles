from django.shortcuts import render, redirect
from django.db import models
from .forms import ProductForm, ClientForm, TransactionPurchaseForm, TransactionSaleForm, SearchForm
from .models import Product, Client, Transaction
from .models import AdminUser
from .forms import LoginForm
from django.http import JsonResponse
from .models import Product, Client


def home(request):
    return render(request, 'store/home.html')

def maintenance_page(request):
    return render(request, 'store/maintenance_page.html')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maintenance_page')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maintenance_page')
    else:
        form = ClientForm()
    return render(request, 'store/add_client.html', {'form': form})

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionPurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maintenance_page')
    else:
        form = TransactionPurchaseForm()
    return render(request, 'store/add_transaction.html', {'form': form})

def add_sale(request):
    if request.method == 'POST':
        form = TransactionSaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maintenance_page')
    else:
        form = TransactionSaleForm()
    return render(request, 'store/add_sale.html', {'form': form})

def search(request):
    form = SearchForm()
    results = {
        'products': [],
        'clients': [],
        'transactions': []
    }

    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        
        results['products'] = Product.objects.filter(
            models.Q(referenceNumber__icontains=query) |
            models.Q(specifications__icontains=query) |
            models.Q(model__icontains=query) |
            models.Q(brand__icontains=query)
        )
        
        # Search in Client
        results['clients'] = Client.objects.filter(
            models.Q(firstName__icontains=query) |
            models.Q(lastName__icontains=query) |
            models.Q(emailAddress__icontains=query) |
            models.Q(contactNumber__icontains=query)
        )
        
        # Search in Transaction
        results['transactions'] = Transaction.objects.filter(
            models.Q(transactionDate__icontains=query) |
            models.Q(totalPrice__icontains=query)
        )

    return render(request, 'store/search.html', {'form': form, 'results': results})

def login_view(request):
    error_message = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = AdminUser.objects.get(username=username)
                if user.check_password(password):
                    request.session['admin_logged_in'] = True
                    return redirect('maintenance_page')
                else:
                    error_message = "Invalid password"
            except AdminUser.DoesNotExist:
                error_message = "Invalid username"
    else:
        form = LoginForm()
    return render(request, 'store/login.html', {'form': form, 'error_message': error_message})

from django.http import HttpResponseForbidden

def maintenance_page(request):
    if not request.session.get('admin_logged_in'):
        return redirect('login')
    return render(request, 'store/maintenance_page.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def autocomplete(request):
    if 'term' in request.GET:
        term = request.GET.get('term')
        product_matches = Product.objects.filter(model__icontains=term).values_list('model', flat=True)
        client_matches = Client.objects.filter(firstName__icontains=term).values_list('firstName', flat=True)
        
        results = list(product_matches) + list(client_matches)
        return JsonResponse(results, safe=False)