from django import forms
from django_filters import (
    FilterSet,
    ModelMultipleChoiceFilter,
    OrderingFilter,
    CharFilter
)

from django.contrib.postgres.search import SearchVector, SearchQuery
from product.models import (
    Product,
    Category
)

class ProductFilter(FilterSet):

    category = ModelMultipleChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    order = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('created', 'created'),
        ),
    )

    search = CharFilter(method='search_filter')
    
    def search_filter(self, queryset, name, value):
        search_query = value
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector('title', 'summary', 'genre__title'),
            ).filter(search=SearchQuery(search_query))
        return queryset

    class Meta:
        model = Product
        fields = ['category', 'search']
