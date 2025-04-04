from django.urls import path
from .views import home, search, add_product, add_client, add_transaction, add_sale, maintenance_page, login_view, logout_view, autocomplete

urlpatterns = [
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('add_product/', add_product, name='add_product'),
    path('add_client/', add_client, name='add_client'),
    path('add_transaction/', add_transaction, name='add_transaction'),
    path('add_sale/', add_sale, name='add_sale'),
    path('maintenance/', maintenance_page, name='maintenance_page'),
    path('login/', login_view, name='login'),
    path('maintenance/', maintenance_page, name='maintenance_page'),
    path('logout/', logout_view, name='logout'),
    path('autocomplete/', autocomplete, name='autocomplete')
]
