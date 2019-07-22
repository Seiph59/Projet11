""" File test dedicated for models in food application """
from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from food.models import Food, Category


class FoodModelTest(TestCase):
    """ Class for test Food Models """

    def setUp(self):
        """ Executed each test """
        self.first_food = Food.objects.create(pk=1,
                               name="test",
                               nutriscore="a",
                               url="www.off.com",
                               url_picture="www.off.com",
                               fat_100g=0.2,
                               saturated_fat_100g=0.1,
                               sugars_100g=0.7,
                               salt_100g=0.5,
                               fat_level="low",
                               salt_level="low",
                               saturated_fat_level="medium",
                               sugars_level="high",
                               last_modified=datetime(2015, 6, 15),
                               openff_id=125452)

        category, _ = Category.objects.get_or_create(name='category')
        self.first_food.categories.add(category)
        self.first_food.save()

        self.second_food = Food.objects.create(pk=2,
                               name="test2",
                               nutriscore="c",
                               url="www.offf.com",
                               url_picture="www.offf.com",
                               fat_100g=0.2,
                               saturated_fat_100g=0.1,
                               sugars_100g=0.7,
                               salt_100g=0.5,
                               fat_level="low",
                               salt_level="low",
                               saturated_fat_level="medium",
                               sugars_level="high",
                               last_modified=datetime(2015, 6, 15),
                               openff_id=125454)

        category, _ = Category.objects.get_or_create(name='category1')
        self.second_food.categories.add(category)
        self.second_food.save()


        self.third_food = Food.objects.create(pk=3,
                               name="test3",
                               nutriscore="a",
                               url="www.offf.com",
                               url_picture="www.offf.com",
                               fat_100g=0.2,
                               saturated_fat_100g=0.1,
                               sugars_100g=0.7,
                               salt_100g=0.5,
                               fat_level="low",
                               salt_level="low",
                               saturated_fat_level="medium",
                               sugars_level="high",
                               last_modified=datetime(2015, 6, 15),
                               openff_id=125414)

        category, _ = Category.objects.get_or_create(name='category1')
        self.third_food.categories.add(category)
        self.third_food.save()


        self.user = User.objects.create(pk=1,
                         username="test",
                         first_name="Al",
                         last_name="taga",
                         email="albg@sfr.fr",
                         password="kevin1234")

    def test_saving_and_retrieving_food(self):
        """ test to check if the food is well saved
        and able to retrieve it """
        saved_food = Food.objects.all()
        self.assertEqual(saved_food.count(), 3)

    def test_link_favorite_food_to_user(self):
        """ Test to see if the favorite food for
        user works """
        food_selected = Food.objects.get(pk=1)
        user_selected = User.objects.get(pk=1)
        food_selected.favorite_users.add(user_selected)
        favorite_added = user_selected.favorite_foods.all()
        self.assertEqual(favorite_added.count(), 1)

    def test_get_substitutes_do_not_have_substitute(self):
        """ Test to check if the classmethod
        works if there is no substitute for
        the product researched"""
        substitute_list, _, _ = Food.get_substitute("test")
        self.assertEqual(len(substitute_list), 1)

    def test_get_substitutes_do_not_find_food(self):
        """ Test to check if the classmethod
        works if there is no food found"""
        food_search = Food.get_substitute("Nutella")
        self.assertEqual(food_search, False)

    def test_get_substitute(self):
        """ Test to find a substitute"""
        substitute_list, _, _ = Food.get_substitute("test2")
        self.assertEqual(len(substitute_list), 2)