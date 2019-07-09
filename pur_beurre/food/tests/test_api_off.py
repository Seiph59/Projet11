from django.test import TestCase
from ..openff_api import Database
from food.models import Food, Category
import requests_mock

class PopulateDbFromApi(TestCase):
    """ Test for all the data insertion from the OpenFoodFacts API"""
    response_expected = {"page_size":"20",
                         "count":75,"page":"1",
                         "skip":0,
                         "products":[{"id":"3034470003107",
                                    "product_name_fr":"Benco original",
                                    "categories":"Boissons, Snacks, Petit-déjeuners, Snacks sucrés, Boissons chaudes, Chocolats, Boissons instantanées, Cacaos et chocolats en poudre, Chocolats en poudre, Boissons avec sucre ajouté, Boissons sans sucre ajouté",
                                    "product_name":"Benco original",
                                    "last_modified_t":1558869123,
                                    "nutrition_grade_fr":"e",
                                    "image_front_url":"https://static.openfoodfacts.org/images/products/303/447/000/3107/front_fr.58.400.jpg",
                                    "url":"https://world.openfoodfacts.org/product/3034470003107/benco-original",
                                    "nutriments":{"fat_100g":2.2,"salt_100g":0.22,"sugars_100g":78,"saturated-fat_100g":1.4},
                                    "nutrient_levels":{"sugars":"high","fat":"moderate","saturated-fat":"moderate","salt":"moderate"},
                                    },
                                    {"id":"3175681851832",
                                    "product_name_fr":"Barre Amande Gerblé - 150 g",
                                    "categories":"Snacks, Sweet snacks, Confectioneries, Bars, Christmas foods and drinks, Christmas sweets, Almond paste, Marzipan, fr:Barres aux fruits",
                                    "product_name":"Barre d'amande Gerblé",
                                    "last_modified_t":1558869125,
                                    "nutrition_grade_fr":"d",
                                    "image_front_url":"https://static.openfoodfacts.org/images/products/317/568/185/1832/front_fr.6.400.jpg",
                                    "url":"https://world.openfoodfacts.org/product/3175681851832/barre-amande-gerble",
                                    "nutriments":{"fat_100g":13,"salt_100g":0.1,"sugars_100g":53,"saturated-fat_100g":1.2},
                                    "nutrient_levels":{"sugars":"high","fat":"moderate","saturated-fat":"low","salt":"low"},
                                    },
                                    {"id":"5449000000996",
                                    "product_name_fr":"Coca Cola - 330 ml",
                                    "categories":" Beverages, Carbonated drinks, Non-Alcoholic beverages, Sodas, Colas, Sweetened beverages, pl:zawiera-kofeinę",
                                    "product_name":"Benco original",
                                    "last_modified_t":1558869128,
                                    "nutrition_grade_fr":"e",
                                    "image_front_url":"https://static.openfoodfacts.org/images/products/544/900/000/0996/front_en.193.400.jpg",
                                    "url":"https://world.openfoodfacts.org/product/5449000000996/coca-cola",
                                    "nutriments":{"fat_100g":0,"salt_100g":0,"sugars_100g":10.6,"saturated-fat_100g":0},
                                    "nutrient_levels":{"sugars":"high","fat":"low","saturated-fat":"low","salt":"low"},
                                    }]
                        }

    def test_get_product_name(self):
        """Unit Test for the "get_product_name" class method"""
        args = {"product_name_fr": "Coca Cola - 330 ml",
         'product_name': "Coca Cola - 330 ml"}
        db = Database()
        result = db.get_product_name(args)
        self.assertEqual(result, 'Coca Cola - 330 ml')

    def test_get_product_name_no_french_name(self):
        """Unit Test for the "get_product_name" class method"""
        args = {'product_name': "Coca Cola - 330 ml"}
        db = Database()
        result = db.get_product_name(args)
        self.assertEqual(result, 'Coca Cola - 330 ml')

    def test_populate_db_foods_and_categories_added(self):
        """ Integration test to check that each food is correctly added
        in the database """
        with requests_mock.Mocker() as m:
            m.get('https://fr.openfoodfacts.org/cgi/search.pl', json=self.response_expected)
            db = Database()
            db.populate()
        self.assertEqual(Food.objects.count(),3)
        self.assertEqual(Category.objects.count(), 27)



