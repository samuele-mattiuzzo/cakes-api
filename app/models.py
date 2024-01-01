from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum

from .const import (CAKE_COMMENT_MAX_LENGTH, CAKE_NAME_MAX_LENGTH,
                    YUM_RATING_MAX_VALUE, YUM_RATING_MIN_VALUE)


class OrderedModel(models.Model):
    class Meta:
        ordering = ['pk']
        abstract = True


class Cake(OrderedModel):
    """
        Cake model
    """
    name = models.CharField(
        max_length=CAKE_NAME_MAX_LENGTH
    )
    comment = models.CharField(
        max_length=CAKE_COMMENT_MAX_LENGTH
    )
    imageUrl = models.URLField()

    @property
    def yumFactor(self):
        rating_count = self.yumrating_set.count()
        if rating_count == 0:
            return 1

        rating = self.yumrating_set.aggregate(
            Sum('rating')
        )

        return round(
            rating['rating__sum'] / rating_count
        )


class YumRating(OrderedModel):
    """
        YumRating model
        Accepts 1,2,3,4 and 5 as values
        Defaults to 1
    """
    cake = models.ForeignKey(
        Cake,
        on_delete=models.CASCADE
    )

    rating = models.PositiveSmallIntegerField(
        default=YUM_RATING_MIN_VALUE,
        validators=[
            MinValueValidator(YUM_RATING_MIN_VALUE),
            MaxValueValidator(YUM_RATING_MAX_VALUE)
        ]
    )
