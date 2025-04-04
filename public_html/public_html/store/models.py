from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Product(models.Model):
    PRODUCT_TYPES = [
        ('Bike', 'Bike'),
        ('Accessory', 'Accessory')
    ]
    referenceNumber = models.CharField(max_length=100, unique=True, default='REF000')
    productType = models.CharField(max_length=20, choices=PRODUCT_TYPES, default='Bike')
    specifications = models.TextField(default='No specifications available')
    releaseYear = models.PositiveIntegerField(default=2020)
    model = models.CharField(max_length=100, default='Default Model')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    brand = models.CharField(max_length=100, default='Generic Brand')

    def __str__(self):
        return self.model

class Bike(models.Model):
    BIKE_TYPES = [
        ('BMX', 'BMX'),
        ('Mountain', 'Mountain'),
        ('Road', 'Road'),
        ('Hybrid', 'Hybrid'),
        ('Cruiser', 'Cruiser'),
        ('Electric', 'Electric')
    ]
    bike = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    bikeType = models.CharField(max_length=20, choices=BIKE_TYPES, default='Mountain')

    def __str__(self):
        return f'{self.bike.model} ({self.bikeType})'

class Accessory(models.Model):
    ACCESSORY_TYPES = [
        ('Helmet', 'Helmet'), ('Lights', 'Lights'), ('Lock', 'Lock'),
        ('Basket', 'Basket'), ('Pump', 'Pump'), ('Bell', 'Bell'),
        ('Wheels', 'Wheels'), ('Handlebars', 'Handlebars'),
        ('Chains', 'Chains'), ('Saddle', 'Saddle'), ('Brakes', 'Brakes')
    ]
    accessory = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    accessoryType = models.CharField(max_length=20, choices=ACCESSORY_TYPES, default='Helmet')

    def __str__(self):
        return f'{self.accessory.model} ({self.accessoryType})'

class Client(models.Model):
    firstName = models.CharField(max_length=100, default='First Name')
    lastName = models.CharField(max_length=100, default='Last Name')
    contactNumber = models.CharField(max_length=20, default='0000000000')
    emailAddress = models.EmailField(unique=True, default='example@example.com')
    address = models.TextField(default='No address provided')
    isBuyer = models.BooleanField(default=False)
    isSeller = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

class Transaction(models.Model):
    transactionDate = models.DateField(auto_now_add=True)
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default = '')

    def __str__(self):
        return f'Transaction #{self.id} - {self.transactionDate}'

class Sale(models.Model):
    SALE_TYPES = [
        ('Online', 'Online'),
        ('InStore', 'InStore')
    ]
    sale = models.OneToOneField(Transaction, on_delete=models.CASCADE, primary_key=True)
    saleType = models.CharField(max_length=20, choices=SALE_TYPES, default='InStore')
    trackingID = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Sale #{self.sale.id}'

class LineItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'LineItem for {self.product.model}'

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Inventory for {self.product.model}'

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchaseDate = models.DateField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Purchase of {self.product.model}'

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    imageURL = models.CharField(max_length=255, default='images/default.jpg')
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Image for {self.product.model}'

class AdminUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)  # Store hashed password

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username
