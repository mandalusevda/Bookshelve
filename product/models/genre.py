from django.db import models
from django.conf import settings
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    FileExtensionValidator
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from safedelete.models import (
    SOFT_DELETE
)
from product.upload import upload_to

class Genre(models.Model):
    _safedelete_policy = SOFT_DELETE

    class Meta:
        verbose_name = _("Genre"),
        verbose_name_plural = _("Genres")

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
    def __str__(self):
        return self.title
    
    def __repr__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("product:genre-products", kwargs={"slug": self.slug})
    
