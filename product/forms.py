from django import forms  
from django.utils.translation import gettext_lazy as _
from product.models import Product 

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Title')})
        self.fields['summary'].widget.attrs.update({'class': 'form-control', 'placeholder': _('summary')})
        self.fields['is_active'].widget.attrs.update({'class': 'form-control', 'placeholder': _('is_active')})
        self.fields['is_special'].widget.attrs.update({'class': 'form-control', 'placeholder': _('is_special')})
        self.fields['stock'].widget.attrs.update({'class': 'form-control', 'placeholder': _('stock')})
        self.fields['rating'].widget.attrs.update({'class': 'form-control', 'placeholder': _('rating')})
        self.fields['category'].widget.attrs.update({'class': 'form-control', 'placeholder': _('category')})
        self.fields['picture'].widget.attrs.update({'class': 'form-control', 'placeholder': _('picture')})

    def save(self, commit=True):
        create_form = super().save(commit=False)
        if commit:
            create_form.save()
        return create_form

    class Meta:
        model = Product
        fields = [
            'title',
            'summary',
            'is_active',
            'is_special',
            'stock',
            'rating',
            'category',
            'picture',
        ]
