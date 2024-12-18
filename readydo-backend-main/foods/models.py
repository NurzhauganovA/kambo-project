from django.db import models
from django.db.models import CASCADE
from imagekit import processors
from imagekit.models import ProcessedImageField

from auth_user.models import User
from common.models import BaseModel


class CuisineTypes(models.IntegerChoices):
    ITALIAN = 1, 'Italian'
    JAPAN = 2, 'Japan'
    CHINESE = 3, 'Chinese'
    KOREAN = 4, 'Korean'
    RUSSIAN = 5, 'Russian'
    KAZAKH = 6, 'Kazakh'
    GEORGIAN = 7, 'Georgian'
    TURKISH = 8, 'Turkish'
    MEXICAN = 9, 'Mexican'
    UZBEK = 10, 'Uzbek'
    THAI = 11, 'Thai'
    INDIAN = 12, 'Indian'
    AMERICAN = 13, 'American'
    CAUCASIAN = 14, 'Caucasian'


class TasteTypes(models.IntegerChoices):
    Spicy = 1, 'Spicy'
    Salty = 2, 'Salty'
    Sweet = 3, 'Sweet'
    Sour = 4, 'Sour'


class Food(BaseModel):
    name = models.CharField(max_length=150, null=False)
    price = models.PositiveIntegerField(null=False)
    user = models.ForeignKey(User, on_delete=CASCADE, null=False)
    ingredients = models.TextField(max_length=400, blank=True)
    cuisine = models.PositiveIntegerField(choices=CuisineTypes, default=CuisineTypes.KAZAKH)
    taste = models.PositiveIntegerField(choices=TasteTypes, default=TasteTypes.Spicy)
    grade = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    photo = ProcessedImageField(
        upload_to='foods/',
        processors=[processors.Transpose()],  # transpose - to fix the 90˚ rotation issue
        options={'quality': 60},
        null=True,
        blank=True)


class Favorites(BaseModel):
    food = models.ForeignKey(Food, on_delete=CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=CASCADE, null=False)


class EstimationTypes(models.IntegerChoices):
    CHEF = 1, 'chef'
    FOOD = 2, 'food'


class Estimation(BaseModel):
    user = models.ForeignKey(User, on_delete=CASCADE, null=False)
    grade = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    type = models.PositiveIntegerField(choices=EstimationTypes, null=False)
    value_id = models.PositiveIntegerField(default=1)
