""" models file dedicated for food application """
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """ Create Category model """
    name = models.CharField(max_length=200)


class Food(models.Model):
    """ Create Food model """
    name = models.CharField(max_length=200)
    nutriscore = models.CharField(max_length=1)
    url = models.URLField(max_length=250)
    url_picture = models.URLField(max_length=250)
    fat_100g = models.DecimalField(max_digits=5, decimal_places=2)
    saturated_fat_100g = models.DecimalField(max_digits=5, decimal_places=2)
    sugars_100g = models.DecimalField(max_digits=5, decimal_places=2)
    salt_100g = models.DecimalField(max_digits=5, decimal_places=2)
    fat_level = models.CharField(max_length=10)
    salt_level = models.CharField(max_length=10)
    saturated_fat_level = models.CharField(max_length=10)
    sugars_level = models.CharField(max_length=10)
    last_modified = models.DateField()
    openff_id = models.BigIntegerField()
    categories = models.ManyToManyField(Category)
    favorite_users = models.ManyToManyField(User, related_name="favorite_foods")

    @staticmethod
    def get_substitute(product_name):
        """ Method which find the substitute of
        the food requested """
        food_requested = Food.objects.filter(name__icontains=product_name)
        if len(food_requested) == 0:
            return False
        name_product = food_requested[0].name
        image = food_requested[0].url_picture
        categories = food_requested[0].categories.all()
        if len(categories) == 0:
            error= ["Pas d'aliment substitut"]
            return [error, name_product, image]
        category_id = categories[0].id
        category_get = Category.objects.filter(pk=category_id)
        substitutes_ordered = category_get[0].food_set.all().order_by('nutriscore')
        return [substitutes_ordered, name_product, image]
