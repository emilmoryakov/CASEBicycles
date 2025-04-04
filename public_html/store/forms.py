from django import forms
from .models import Product, Bike, Accessory, Client, Transaction, Sale, LineItem

class ProductForm(forms.ModelForm):
    bikeType = forms.ChoiceField(choices=Bike.BIKE_TYPES, required=False)
    accessoryType = forms.ChoiceField(choices=Accessory.ACCESSORY_TYPES, required=False)

    class Meta:
        model = Product
        fields = ['productType', 'referenceNumber', 'specifications', 'releaseYear', 'model', 'price', 'brand']

    def save(self, commit=True):
        product = super().save(commit=commit)

        if self.cleaned_data['productType'] == 'Bike':
            bike = Bike(bike=product, bikeType=self.cleaned_data['bikeType'])
            bike.save()
        elif self.cleaned_data['productType'] == 'Accessory':
            accessory = Accessory(accessory=product, accessoryType=self.cleaned_data['accessoryType'])
            accessory.save()

        return product

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['firstName', 'lastName', 'contactNumber', 'emailAddress', 'address', 'isBuyer', 'isSeller']

class TransactionPurchaseForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField()
    price = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Transaction
        fields = ['totalPrice', 'client']

    def save(self, commit=True):
        transaction = super().save(commit=commit)

        line_item = LineItem(
            transaction=transaction,
            product=self.cleaned_data['product'],
            quantity=self.cleaned_data['quantity'],
            price=self.cleaned_data['price']
        )
        line_item.save()

        return transaction

class TransactionSaleForm(forms.ModelForm):
    saleType = forms.ChoiceField(choices=Sale.SALE_TYPES)
    trackingID = forms.CharField(required=False)

    class Meta:
        model = Transaction
        fields = ['totalPrice', 'client']

    def save(self, commit=True):
        transaction = super().save(commit=commit)

        sale = Sale(
            sale=transaction,
            saleType=self.cleaned_data['saleType'],
            trackingID=self.cleaned_data['trackingID']
        )
        sale.save()

        return transaction

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
    

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

