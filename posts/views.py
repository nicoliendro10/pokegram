import requests
import json

from django.shortcuts import render


def list_posts(request):
    pokemons_list = []
    pokemons_request = requests.get("https://pokeapi.co/api/v2/pokemon?limit=5")
    pokemons_dict = json.loads(pokemons_request.content)
    for pokemon in pokemons_dict['results']:
        pokemon_info_request = requests.get(pokemon['url'])
        pokemon_info_dict = json.loads(pokemon_info_request.content)
        pokemon_data_dict = {
            'name': pokemon_info_dict['name'],
            'photo': pokemon_info_dict['sprites']['other']['official-artwork']['front_default'],
            'height': pokemon_info_dict['height'],
            'weight': pokemon_info_dict['weight']
        }
        pokemons_list.append(pokemon_data_dict)
    return render(request, 'feed.html', {'pokemons_list': pokemons_list})

