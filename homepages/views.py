from django.db import connection
from django.shortcuts import render
from homepages.models import PokemonInfo, PokemonType
# Create your views here.

def indexPageView(request):
    if request.method == "GET" and "pokemon" in request.GET:
        pokemons = PokemonInfo.objects.filter(name__icontains=request.GET['pokemon'])
    else:
        pokemons = PokemonInfo.objects.all()
    data = {
        'pokemons': pokemons
    }
    return render(request, 'homepages/index.html', data)

def detailsPageView(request, pokemon):
    pokemon_obj = PokemonInfo.objects.get(pokemon_id=pokemon)
    #type = PokemonType.objects.filter(pokemon__in=pokemon)
    cursor = connection.cursor()
    query = "SELECT type FROM pokemon_type WHERE pokemon_id=%s"
    cursor.execute(query, [pokemon])
    columns = [col[0] for col in cursor.description]
    type = [dict(zip(columns, row)) for row in cursor.fetchall()]
    data = {
        'pokemon': pokemon_obj,
        'type': type,
    }
    return render(request, 'homepages/details.html', data)

def showPokemonPageView(request):
    data = PokemonInfo.objects.all()
    context = {
        "poke" : data
    }
    return render(request, 'homepages/showPokemon.html', context)

def showSinglePokemonPageView(request, poke_id):
    data = PokemonInfo.objects.get(pokemon_id = poke_id)

    context = {
        "record": data,
    }

    return render(request, 'homepages/editPokemon.html', context)

def updatePokemonPageView(request):
    if request.method == "POST":
        poke_id = request.POST['poke_id']

        pokemon = PokemonInfo.objects.get(pokemon_id=poke_id)

        pokemon.first_name = request.POST['poke_name']
        pokemon.last_name = request.POST['poke_type']

        pokemon.save()
    return showPokemonPageView(request)

def deletePokemonPageView(request, poke_id):
    data = PokemonInfo.objects.get(pokemon_id = poke_id)
    data.delete()
    return showPokemonPageView(request)

def addPokemonPageView(request):
    if request.method == "POST":

        pokemon = PokemonInfo()

        pokemon.first_name = request.POST['poke_name']
        pokemon.last_name = request.POST['poke_type']
        

        pokemon.save()
        return showPokemonPageView(request)
    else:
        return render(request, 'homepages/addPokemon.html')




