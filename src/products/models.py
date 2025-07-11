from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Product(models.Model):
    name = models.CharField(_("Название"), max_length=255)
    price = models.DecimalField(_("Цена"), max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        _("Цена со скидкой"), max_digits=10, decimal_places=2
    )
    rating = models.IntegerField(_("Рейтинг"), null=True, blank=True)
    review_count = models.IntegerField(_("Количество отзывов"), null=True, blank=True)

    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")
