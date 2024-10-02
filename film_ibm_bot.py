import os
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

IMDB_API_KEY = os.getenv("IMDB_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

mistral_client = Mistral(api_key=MISTRAL_API_KEY)

def get_movie_info(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={IMDB_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['Response'] == 'True':
            return {
                'Title': data['Title'],
                'Year': data['Year'],
                'IMDb Rating': data['imdbRating'],
                'Plot': data['Plot'],
                'Actors': data['Actors'],
                'Genre': data['Genre']
            }
        else:
            return f"Erreur: {data['Error']}"
    else:
        return f"Erreur HTTP: {response.status_code}"

def get_mistral_summary(plot):
    prompt = f"Voici l'intrigue d'un film : {plot}. Peux-tu me faire un résumé de ce film ?"
    response = mistral_client.ask(prompt)
    return response['output']

def get_mistral_recommendation(user_input):
    prompt = f"Je préfère des films {user_input}. Quels films me recommanderais-tu ?"
    response = mistral_client.ask(prompt)
    return response['output']

class ChatbotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Chatbot de Recommandation de Films')
        self.setGeometry(100, 100, 400, 400)

        # Layout principal
        layout = QVBoxLayout()

        # Label d'instruction
        self.label = QLabel('Entrez le titre d\'un film ou décrivez vos préférences :')
        layout.addWidget(self.label)

        # Champ de saisie utilisateur
        self.input_field = QLineEdit(self)
        layout.addWidget(self.input_field)

        # Bouton pour obtenir des informations sur un film
        self.info_button = QPushButton('Obtenir des informations sur le film', self)
        self.info_button.clicked.connect(self.get_movie_info)
        layout.addWidget(self.info_button)

        # Bouton pour obtenir un résumé via Mistral
        self.summary_button = QPushButton('Obtenir un résumé via Mistral', self)
        self.summary_button.clicked.connect(self.get_summary)
        layout.addWidget(self.summary_button)

        # Bouton pour obtenir des recommandations de films via Mistral
        self.recommend_button = QPushButton('Obtenir des recommandations', self)
        self.recommend_button.clicked.connect(self.get_recommendations)
        layout.addWidget(self.recommend_button)

        # Zone de texte pour afficher les résultats
        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        # Appliquer le layout
        self.setLayout(layout)

    def get_movie_info(self):
        movie_title = self.input_field.text()
        if movie_title:
            movie_info = get_movie_info(movie_title)
            if isinstance(movie_info, dict):
                info_text = (f"Titre : {movie_info['Title']}\n"
                             f"Année : {movie_info['Year']}\n"
                             f"Note IMDb : {movie_info['IMDb Rating']}\n"
                             f"Résumé : {movie_info['Plot']}\n"
                             f"Acteurs : {movie_info['Actors']}\n"
                             f"Genre : {movie_info['Genre']}")
                self.result_area.setText(info_text)
            else:
                self.result_area.setText(movie_info)
        else:
            self.result_area.setText("Veuillez entrer un titre de film.")

    def get_summary(self):
        movie_title = self.input_field.text()
        if movie_title:
            movie_info = get_movie_info(movie_title)
            if isinstance(movie_info, dict):
                summary = get_mistral_summary(movie_info['Plot'])
                self.result_area.setText(f"Résumé de Mistral pour {movie_info['Title']} :\n{summary}")
            else:
                self.result_area.setText(movie_info)
        else:
            self.result_area.setText("Veuillez entrer un titre de film.")

    def get_recommendations(self):
        user_preferences = self.input_field.text()
        if user_preferences:
            recommendations = get_mistral_recommendation(user_preferences)
            self.result_area.setText(f"Recommandations de films basées sur vos goûts :\n{recommendations}")
        else:
            self.result_area.setText("Veuillez décrire vos préférences cinématographiques.")

if __name__ == '__main__':
    app = QApplication([])
    chatbot = ChatbotApp()
    chatbot.show()
    app.exec_()
