from django.shortcuts import render, get_object_or_404, redirect, redirect
from django.urls.base import reverse
from django.views.generic import TemplateView

from django.contrib.auth import login, logout
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm
)
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.views.generic import (
    ListView,
    TemplateView
)
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView

from product.models import (
    Product,
    Category,
    Rating
)
from product.filter import (
    ProductFilter
)
from .forms import ProductForm
User = get_user_model()

class ProductDetailView(TemplateView):
    template_name = "pages/user/page-detail.html"
    page_name = 'product-detail'
    
    def get_context_data(self,*args, **kwargs):
        context= super().get_context_data(**kwargs)
        context['product'] = Product.objects.all().filter(sku = context['sku'])
        return context

class Home_View(ListView):
    template_name = "pages/user/home.html"
    page_name = 'home'
    context_object_name = 'products'
    pagination_choices=['10','15','20']
    
    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        if self.request.GET.get('paginate_by') in self.pagination_choices:
            return self.request.GET.get('paginate_by', self.paginate_by)
        else:
            return 60
    
    def get_queryset(self) -> QuerySet:
        prod_filter=ProductFilter(
            self.request.GET,
            queryset=Product.objects.all().select_related('category'))
        return prod_filter.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(
            self.request.GET,
            queryset=self.get_queryset())
        context['category'] = Category.objects.all()
        context['pagination_choices'] = self.pagination_choices
        return context
    
# @login_required(login_url='product:login')
class page_add(FormView):
    template_name = "pages/user/page_add.html"
    page_name = 'page_list'
    form_class = ProductForm
    # success_url =  reverse_lazy('account:index')

    def get_message(self, level='success'):
        if level == 'success':
            msg = _(
                f"Your message sent successfully! Thank you for contacting us.")
        else:
            msg = _(
                f"Your form has some errors!")
        return msg

    def get_context_data(self,*args, **kwargs) -> dict:
        context= super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context
    
        
    def post(self, request, *args, **kwargs):
        if request.method=="POST":
            products = Product()
            products.title = request.POST['title']
            products.summary = request.POST['summary']
            products.is_active = request.POST['is_active']
            products.created = request.POST['created']
            products.modified = request.POST['modified']
            products.picture =request.FILES['picture']
            products.is_special=request.POST['is_special']
            products.rating = request.POST['rating']
            products.category=Product.objects.get(id=request.POST['category'])
            products.stock = request.POST['stock']
            products.save()
            return redirect('page_list')

# @login_required(login_url='product:login')
class page_list(ListView):
    template_name = "pages/user/page_list.html"
    page_name = 'page_list'
    context_object_name = 'products'
    pagination_choices=['10','15','20']
    
    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        if self.request.GET.get('paginate_by') in self.pagination_choices:
            return self.request.GET.get('paginate_by', self.paginate_by)
        else:
            return 60
    
    def get_queryset(self) -> QuerySet:
        prod_filter=ProductFilter(
            self.request.GET,
            queryset=Product.objects.all().select_related('category'))
        return prod_filter.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(
            self.request.GET,
            queryset=self.get_queryset())
        context['category'] = Category.objects.all()
        context['pagination_choices'] = self.pagination_choices
        return context      
    
    def check_user_rated(request):
        user_ratings = Rating.objects.filter(user=request.user)
        if not user_ratings.exists():
            messages.error(request, "there is not enough data about you")  

    
def rate_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        rating_value = int(request.POST.get('rating'))
        rating = Rating.objects.filter(user=request.user, product=product).first()
        if rating is None:
            rating = Rating(user=request.user, product=product, rating=rating_value)
        else:
            rating.rating = rating_value
        rating.save()

        return redirect('product:page_list')
    return render(request, 'pages/user/rate.html', {'product': product})

@login_required
def recommend_products(request):
    recommended = Product.objects.exclude(rating__user=request.user).order_by('-rating__rating')[:5]
    return render(request, 'pages/user/recommend.html', {'recommended': recommended})
      

def page_edit(request, id):  
    #update view
    products = Product.objects.get(id=id)  
    context ={}
    form = ProductForm(request.POST, instance = products)
    if form.is_valid():  
        form.save()  
        return redirect(reverse('product:page_list'))
    context['form']= form  
    return render(request, 'pages/user/update.html', {'products':products}) 

def retrieve(request,id):
    #retrieve view
    products = Product.objects.all().filter(id=id)
    return render(request,"pages/user/retrieve.html",{'products':products})  

def page_delete(request, id):
    #delete view  
    products = Product.objects.get(id=id)  
    products.delete()  
    return redirect("/page_list")


def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse('product:page_list'))
        else:
            print(form.errors)
    return render(request, 'pages/user/login.html', {'form': form})


@login_required(login_url='product:login')
def log_out(request):
    logout(request)
    return redirect(reverse('product:login'))


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('product:page_list'))
        else:
            print(form.errors)
    return render(request, 'pages/user/register.html', {'form': form})
