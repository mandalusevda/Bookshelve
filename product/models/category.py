from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from safedelete.models import (
    SOFT_DELETE
)

class Category(models.Model):
    _safedelete_policy = SOFT_DELETE

    class Meta:
        verbose_name = _("Category"),
        verbose_name_plural = _("Categories")

    slug = models.SlugField(
        _("slug"),
        max_length=13,
        help_text="label in url for each product",
        unique=True,
        allow_unicode = True,
        editable = True
    )
    title = models.CharField(
        _("Title"), 
        max_length=150,
        help_text = _("Title of each product"),
        unique = True,
    )
    deleted = models.BooleanField(
        _("is deleted"),
        default=False,
        help_text="deleted state of each product",
    )
    is_active = models.BooleanField(
        _("is active"),
        default=False,
        help_text="summary of each product",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created = models.DateTimeField(
        _("created"),
        help_text = _("created date of each product")
    )
    modified = models.DateTimeField(
        _("modified"),
        help_text = _("Modified date time"),
        auto_now = True
    )
    modified_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_("Modified By"),
        help_text = _("Modified by specific user"),
        related_name = "%(app_label)s_%(class)s_related",
        on_delete=models.DO_NOTHING,
    )

    """class MPTTMeta:
        order_insertion_by = ['title']
    """
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title,allow_unicode=True)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.slug
    
    def __repr__(self):
        return self.slug
    
    def get_absolute_url(self):
        return reverse("product:category-products", kwargs={"slug": self.slug})

    @property
    def get_in_stock_products(self):
        return self.products.in_stock().all()
    
    @property
    def get_out_of_stock_products(self):
        return self.products.is_out_of_stock().all()

    @property
    def get_products(self):
        return self.products.all()
    
    @property
    def get_products_count(self):
        return self.products.count()
    
    @property
    def get_active_products(self):
        return self.products.actives().all()
    
    @property
    def get_active_products(self):
        return self.products.actives().all()
    
    @property
    def get_deactive_products(self):
        return self.products.deactives().all()
    
    @property
    def get_specials_products(self):
        return self.products.specials().all()
    
    def automatic_slug_creation(self):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            count = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug

    def save(self, *args, **kwargs):
        self.automatic_slug_creation()
        super().save(*args, **kwargs)
