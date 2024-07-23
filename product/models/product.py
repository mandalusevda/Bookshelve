import random

#for image configs
import os
import io
from pathlib import Path
from PIL import Image
from sorl.thumbnail import get_thumbnail
import eav

from django.db import models
from django.conf import settings
from django.core.files import File
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    FileExtensionValidator
)
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from safedelete.models import (
    SOFT_DELETE
)
from product.upload import upload_to

class Product(models.Model):
    _safedelete_policy = SOFT_DELETE

    class Meta:
        verbose_name = _("Product"),
        verbose_name_plural = _("Products")

    title = models.CharField(
        _("Title"), 
        max_length=150,
        help_text = _("Title of each product"),
        unique = True,
    )
    sku = models.CharField(
        _("sku"),
        max_length=13,
        help_text="unique identity for each product",
        unique=True
    )
    slug = models.SlugField(
        _("slug"),
        max_length=13,
        help_text="label in url for each product",
        unique=True,
        allow_unicode = True,
        editable = True
    )
    subtitle = models.CharField(
        _("subtitle"),
        null=True,
        blank=True,
        max_length=150,
        help_text="subtitle of each product",
        unique=True
    )
    summary = models.CharField(
        _("summary"),
        null=True,
        blank=True,
        max_length=200,
        help_text="summary of each product"
    )
    is_active = models.BooleanField(
        _("is active"),
        default=False,
        help_text="summary of each product",
    )
    is_special = models.BooleanField(
         _("is special"),
        default=False,
        help_text="Special tag of each product",
    )
    deleted = models.BooleanField(
        _("is deleted"),
        default=False,
        help_text="deleted state of each product",
    )
    stock = models.PositiveIntegerField(
        _("stock"),
        default=False,
        help_text="Stock quantity of each product",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        'Category',
        verbose_name=_('Category'),
        related_name='products',
        default='product',        
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    genre = models.ForeignKey(
        'Genre',
        verbose_name=_('Genre'),
        related_name='products',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    rating = models.ForeignKey(
        "Rating",
        related_name="products",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    description = models.TextField(
        _("description"),
        null=True,
        blank=True,
        help_text = _("Long Description of each product")
    )
    created = models.DateTimeField(
        _("created"),
        help_text = _("created date of each product"),
        null=True,
        blank=True,
    )
    modified = models.DateTimeField(
        _("modified"),
        help_text = _("Modified date time"),
        auto_now = True,
        null=True,
        blank=True,
    )
    modified_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_("Modified By"),
        help_text = _("Modified by specific user"),
        related_name = "%(app_label)s_%(class)s_related",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    picture = models.ImageField(
        _("picture"),
        help_text = _("picture of each product"),
        upload_to=upload_to.date_directory_path,
        height_field='height_field',
        width_field='width_field',
        max_length=110,
        validators=[FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'jpg', 'jpeg', 'png'])],
        null=True,
        blank=True,
    )
    alternate_text = models.CharField(
        _("Alternate Text"),
        null=True,
        blank=True,
        max_length=110,
        validators=[
            MaxLengthValidator(150),
            MinLengthValidator(3)
        ]
    )
    width_field = models.PositiveSmallIntegerField(
        _("Width Field"),
        editable=False,
        null=True,
        blank=True,
    )
    height_field = models.PositiveSmallIntegerField(
        _("Height Field"),
        editable=False,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title,allow_unicode=True)
        sku = "".join(random.sample("123456789"*3, k=7))
        if not self.sku:
            self.sku="SWP-{}".format(sku)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sku
    
    def __repr__(self):
        return self.sku
    
    def get_absolute_url(self):
        return reverse("product:product-detail", kwargs={"sku": self.sku, "slug": self.slug})

    def convert_to_webp(self):
        if ".webp" not in self.picture.path:
            path = self.picture.path
            format = Path(path).suffix
            with Image.open(path) as data:
                data= data.convert('RGB')
                output = io.BytesIO()
                data.save(output, format='webp')
                self.picture.save(os.path.basename(path).replace(format,'.webp'), output )

    def convert_to_jpg(self):
        if ".jpg" not in self.picture.path:
            path = self.picture.path
            format = Path(path).suffix

            with Image.open(path) as data:
                data= data.convert('RGB')
                output = io.BytesIO()
                data.save(output, format='JPEG')
                self.picture.save(os.path.basename(path).replace(format,'.jpg'), output )

    def convert_to_png(self):
        if ".png" not in self.picture.path:
            path = self.picture.path
            format = Path(path).suffix
            with File(open(self.picture.path,'rb')) as data:
                self.picture.save(os.path.basename(self.picture.path).replace(format,'.png'), data )
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

    def crop(self ,left, top, right, bottom):
        path = self.picture.path
        with Image.open(path) as pic:
            pic = pic.convert('RGB')
            data = pic.crop((left, top, right, bottom))
            output = io.BytesIO()
            data.save(output, format='JPEG')
            self.picture.save(os.path.basename(path), output )

    def get_picture_size(self):
        return self.picture.size
    
    def get_picture_dimensions(self):
        return (self.picture.width,self.picture.height)
    
    @property
    def get_pic_url(self):
        if self.picture:
            return self.picture.url
        return ''
    
    @property
    def thumbnail(self):
        return get_thumbnail(self.picture, '100x100', crop='center', quality=99)

    @property
    def is_out_of_stock(self):
        if self.stock == 0:
            return True
        return False

    @property
    def list_available_colors(self):
        return self.stock.values_list("color__hex_code")

    def update_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            self.rating = ratings.aggregate(models.Avg('rating'))['rating__avg']
            self.save()
    
 
eav.register(Product)
