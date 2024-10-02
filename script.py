import tweepy
from datetime import datetime, timedelta, timezone

# Remplacer par vos propres clés d'API Twitter
API_KEY = 'AlmNR2od9irCbT1POQthxGkF9'
API_SECRET_KEY = 'KECzk3dTzbhmtXdKIqCiIr5VvfxGXKsxlmnOX6XYXD7SMW6rNb'
ACCESS_TOKEN = '1841116416142966795-3WTYdlH1cvfb1MNnRDGyospRj0272J'
ACCESS_TOKEN_SECRET = 'bHHAb0MxqWw351K9bHVCwFByZdrUs8n9Hk9NcpC5an0Vb'

# Authentification auprès de l'API Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Fonction pour récupérer les tweets des dernières 48 heures
def get_recent_tweets(username):
    # Calculer la date et l'heure d'il y a 48 heures, en utilisant UTC
    time_limit = datetime.now(timezone.utc) - timedelta(hours=48)

    # Récupérer les tweets récents du compte utilisateur
    tweets = api.user_timeline(screen_name=username, count=100, tweet_mode='extended')

    # Filtrer les tweets en fonction de la date
    recent_tweets = [tweet for tweet in tweets if tweet.created_at.replace(tzinfo=timezone.utc) > time_limit]

    # Afficher les tweets
    for tweet in recent_tweets:
        print(f"Tweet de {username} à {tweet.created_at}:")
        print(tweet.full_text)
        print("-" * 80)

# Utilisation de la fonction
if __name__ == "__main__":
    username = "@elonmusk"  # Remplacez par le nom d'utilisateur du compte à surveiller
    get_recent_tweets(username)
