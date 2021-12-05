from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import redirect
import requests
import json

from posts.forms import PostForm
from posts.models import Post
from django.shortcuts import render


def generate_pokemons():
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
    return render(request, 'posts/feed.html', {'pokemons_list': pokemons_list})

class PostsFeedView(LoginRequiredMixin, ListView):

    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created')
    paginate_by = 2
    context_object_name = 'posts'


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:feed')
    else:
        form = PostForm()
    
    return render(
        request,
        'posts/new.html',
        context={
            'form': form,
            'user': request.user,
            'profile': request.user.profile
        }
    )