""" View file for food application """
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.views import View
from food.models import Food


def food_page(request, food_id):
    "function for food_page"
    article = Food.objects.get(pk=food_id)
    return render(request, 'food/food_details.html', {'article': article})



def get(request):
    """ dedicated for get methods """
    template_name = 'food/search_page.html'
    query = request.GET.get('search')
    list = Food.get_substitute(query)
    if list is False:
        return render(request, template_name, {'nofood': "Pas d'aliment trouvé"})
    elif list is "error":
        return render(request, template_name, {'no_substitute': "Votre aliment n'a pas de substitut"})
    substitutes_list = list[0]
    paginator = Paginator(substitutes_list, 6)
    page = request.GET.get('page')
    substitutes_list = paginator.get_page(page)
    args = ({'food_search': list[1],
                'articles_found': substitutes_list,
                'image': list[2],
                'page': page,
                'query': query})
    return render(request, template_name, args)


@require_POST
def favorite(request):
    """ Receive the ajax request to add favorite foods"""
    if request.is_ajax():
        food_id = json.loads(request.body.decode('utf-8')).get('id')
        food = Food.objects.get(pk=food_id)
        current_user = request.user
        user = User.objects.get(pk=current_user.id)
        food.favorite_users.add(user.id)
        data = "le produit a été enregistré"
    return HttpResponse(data)

@login_required
def my_foods(request):
    """ display the page my_foods """
    foods_saved = request.user.favorite_foods.all()
    paginator = Paginator(foods_saved, 6)
    page = request.GET.get('page')
    foods_saved = paginator.get_page(page)
    return render(request, 'food/my_foods.html', {'foods_saved': foods_saved})
