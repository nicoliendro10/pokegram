from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
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

class PostDetailView(LoginRequiredMixin, DetailView):

    template_name = 'posts/detail.html'
    queryset = Post.objects.all()
    context_object_name = 'post'

class CreatePostView(LoginRequiredMixin, CreateView):

    template_name = 'posts/new.html'
    form_class = PostForm
    success_url = reverse_lazy('posts:feed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
        return context
    