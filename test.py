import requests

# Clé API obtenue via l'inscription à OMDb
OMDB_API_KEY = '6445ade7'

# Titre du film à rechercher
movie_title = "inception"

# URL de l'API OMDb en utilisant le paramètre 't' pour le titre
url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"

# Effectuer une requête GET à l'API OMDb
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Extraire les informations JSON
    data = response.json()
    if data['Response'] == 'True':
        print(f"Titre : {data['Title']}")
        print(f"Année : {data['Year']}")
        print(f"Note IMDb : {data['imdbRating']}")
        print(f"Résumé : {data['Plot']}")
    else:
        print(f"Erreur : {data['Error']}")
else:
    print(f"Erreur HTTP : {response.status_code}")
