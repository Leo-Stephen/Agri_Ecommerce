# product_app/forms.py

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'quantity', 'description', 'image', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Product Name'
            }),
            'category': forms.Select(attrs={
                'class': 'form-input'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-input price-input',
                'min': '10',
                'step': '1',
                'placeholder': '0.00'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '1',
                'placeholder': 'Available Quantity'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': 'Product Description'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            })
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero")
        return price

    def clean_image(self):
            image = self.cleaned_data.get('image')
            if image:
                if image.size > 5 * 1024 * 1024:  # 5MB limit
                    raise forms.ValidationError("Image file too large ( > 5MB )")
            return image
