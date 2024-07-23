from django.contrib import admin
from django.utils.safestring import mark_safe
from product.models import (
    Product,
    Category,
    Genre,
    Rating
)
from product.traditional import (
    MyProductAdmin
)
from safedelete.admin import (
    SafeDeleteAdmin, 
    highlight_deleted, 
    SafeDeleteAdminFilter
)
from simple_history.admin import SimpleHistoryAdmin
from rangefilter.filters import (
    DateRangeFilter, 
    DateTimeRangeFilter
)
from mptt.admin import (
    DraggableMPTTAdmin,
    TreeRelatedFieldListFilter,
)
from django_mptt_admin.admin import DjangoMpttAdmin

"""class PackAdminInline(admin.StackedInline):
    model = Pack
    extra = 0"""

@admin.register(Category)
class CategoryAdmin(SimpleHistoryAdmin, SafeDeleteAdmin): 
    list_display = (
        highlight_deleted,
        'title',
        'is_active',
        #'parent',
        'created',
        'modified',
        'modified_by',
    )+ SafeDeleteAdmin.list_display

    list_filter = (
        'is_active',
        ('created',DateRangeFilter),
        ('modified',DateTimeRangeFilter),
        'modified_by',
    )+ SafeDeleteAdmin.list_filter
    readonly_fields = ['slug', 'modified']
    search_fields = ['slug','title']
    empty_value_display = '-N/A-'
    list_editable = ['title']
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title',
                'slug',
            )
        }),
        ('Category Availability', {
            'classes': ('collapse',),
            'fields': (
                'is_active',
            ),
        }),
        ('Security Center', {
            'classes': ('collapse',),
            'fields': (
                'created',
                'modified',
                'modified_by'
            ),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)
    
    @admin.display(description='title')
    def display_title(self,obj):
        return (obj.title[:50]+'..')if len(obj.title)>50 else obj.title
    

@admin.register(Genre)
class GenreAdmin(SimpleHistoryAdmin):
    list_display = (
        highlight_deleted,
        'title'
    )
    search_fields = ['title']
    history_list_display = ['title']
    readonly_fields = ['slug']
    
    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Product)
class ProductAdmin(SafeDeleteAdmin):  
    list_display = (
        'subtitle',
        'title',
        'summary',
        'is_active',
        'is_special',
        'stock',
        'get_average_rating',
        'description',
        'created',
        'modified',
        'modified_by',
        'picture',
        'alternate_text',
        'category',
        'get_genre'
    ) + SafeDeleteAdmin.list_display

    list_filter = (
        'is_active',
        'is_special',
        ('created', DateRangeFilter),
        ('modified', DateTimeRangeFilter),
    ) + SafeDeleteAdmin.list_filter

    search_fields = ['sku', 'title', 'summary']
    history_list_display = ["stock", 'is_active', 'is_special']
    empty_value_display = '-N/A-'
    list_editable = ['stock', 'title']
    readonly_fields = ['sku', 'slug', 'modified', 'modified_by']
    raw_id_fields = ['category']  # must be a foreign key or a many-to-many field

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'sku',
                'title',
                'slug',
                'category',
                'genre'
            )
        }),
        ('Product Information', {
            'classes': ('collapse',),
            'fields': (
                'picture',
                ('summary', 'subtitle'),
                'description',
            ),
        }),
        ('Ratings', {
            'fields': (
                'rating',
            )
        }),
        ('Product Availability', {
            'classes': ('collapse',),
            'fields': (
                'is_active',
                'is_special',
                'stock'
            ),
        }),
        ('Security Center', {
            'classes': ('collapse',),
            'fields': (
                'created',
                'modified',
                'modified_by'
            ),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)
    
    @admin.display(description='Title')
    def display_title(self, obj):
        return (obj.title[:50] + '..') if len(obj.title) > 50 else obj.title
    
    @admin.display(description='Status')
    def display_status(self, obj):
        parameters = ('#f46a6a', 'Out of stock') if obj.stock == 0 else ('#1e9368', 'Available')
        data_point = '<span style="color: {};">{}</span>'.format(*parameters)
        return mark_safe(data_point)
    
    @admin.display(description='Created', ordering='created')
    def display_created(self, obj):
        return obj.created.strftime('%Y-%m-%d')

    @admin.display(description='Modified', ordering='modified')
    def display_modified(self, obj):
        return obj.modified.strftime('%Y-%m-%d')

    @admin.display(description='Average Rating')
    def get_average_rating(self, obj):
        return int(obj.rating.rating) if obj.rating else 'No Rating'

    @admin.display(description='Genre')
    def get_genre(self, obj):
        return obj.genre.title if obj.genre else 'No Genre'
    
@admin.register(Rating)
class RatingAdmin(SimpleHistoryAdmin, SafeDeleteAdmin):
    list_display = (
        'message',
        'product',
        'rating',
        'user',
    )
    list_filter = (
        'user',
        'rating',
    )
    raw_id_fields = ['product']
    search_fields = ['message']
    save_on_top = True
    list_per_page = 25
    readonly_fields = ['user']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description='product')
    def display_product(self, obj):
        product_title = Product.objects.filter(
            sku=obj.product).values('title').first()
        return product_title['title']
