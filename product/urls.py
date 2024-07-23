from django.urls import(
    path,
    re_path
)

from product import views

app_name = 'product'
urlpatterns = [
    path('',views.Home_View.as_view(),name='home'),
    path('page_list',views.page_list.as_view(),name='page_list'),
    path('page_add', views.page_add.as_view(),name='page_add'),  
    path('update/<int:id>', views.page_edit,name='page_edit'),
    path('retrieve/<int:id>', views.retrieve),    
    path('delete/<int:id>', views.page_delete),  
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('rate/<int:id>', views.rate_product, name='rate_product'),
    path('recommend/', views.recommend_products, name='recommend_products'),
    #path('product-detail/<str:sku>/', views.ProductDetailView.as_view(), name = "product-detail"),
    #re_path(r'product-detail/(?P<sku>[-\w]+)/(?P<slug>[-\w]+)/', views.ProductDetailView.as_view(), name = "product-detail"),

]