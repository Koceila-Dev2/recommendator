from flask import Flask, render_template, request, session
from dotenv import load_dotenv
import os
from mistralai import Mistral

# Charger les variables d'environnement
load_dotenv()
api_key = os.getenv("API_KEY")

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")  # Clé pour la session

# Initialiser le client Mistral
client = Mistral(api_key=api_key)
model = "mistral-large-latest"

# Liste des questions à poser
questions = [
    "Quel genre de films aimes-tu le plus ? (par exemple : action, comédie, drame, science-fiction, horreur...)",
    "As-tu un acteur ou un réalisateur préféré dont tu apprécies particulièrement les films ?",
    "Quel est le dernier film que tu as vu et que tu as vraiment aimé ?",
    "Tu préfères les films légers et divertissants, ou plutôt ceux qui sont plus sérieux et intenses ?",
    "Tu préfères les films avec des intrigues complexes ou ceux qui sont plus impressionnants visuellement ?"
]

@app.route('/')
def index():
    return render_template('movie_finder.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form['prompt']

    # Initialiser la session pour stocker les réponses si elle n'existe pas
    if 'conversation_stage' not in session:
        session['conversation_stage'] = 0
        session['user_answers'] = []

    # Récupérer l'étape actuelle de la conversation
    conversation_stage = session['conversation_stage']
    user_answers = session['user_answers']

    # Ajouter la réponse de l'utilisateur à la liste des réponses
    if conversation_stage > 0:
        user_answers.append(user_input)
        session['user_answers'] = user_answers

    # Poser la question suivante ou générer le top 5 après la dernière question
    if conversation_stage < len(questions):
        next_question = questions[conversation_stage]
        conversation_stage += 1
        session['conversation_stage'] = conversation_stage
        return render_template('movie_finder.html', user_input=user_input, response_text=next_question)

    else:
        # Construire le prompt pour demander à l'API Mistral de générer un top 5 de films en fonction des réponses
        conversation_prompt = (
            "Tu es un expert en cinéma. L'utilisateur a répondu aux questions suivantes pour que tu puisses lui recommander 5 films :\n"
            f"1. Genre préféré : {user_answers[0]}\n"
            f"2. Acteur ou réalisateur préféré : {user_answers[1]}\n"
            f"3. Dernier film apprécié : {user_answers[2]}\n"
            f"4. Préférence tonale (léger ou intense) : {user_answers[3]}\n"
            f"5. Intrigue complexe ou visuel impressionnant : {user_answers[4]}\n"
            "Sur cette base, propose un top 5 de films qui correspondent aux goûts de l'utilisateur, avec une brève explication pour chaque film."
        )

        # Appeler l'API Mistral pour générer la réponse
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {"role": "system", "content": "Tu es un expert en cinéma qui aide à recommander des films."},
                {"role": "user", "content": conversation_prompt}
            ]
        )

        # Extraire la réponse du modèle
        response_text = chat_response.choices[0].message.content

        # Réinitialiser la session après avoir donné le top 5
        session.pop('conversation_stage', None)
        session.pop('user_answers', None)

        # Retourner la réponse générée par l'API
        return render_template('movie_finder.html', user_input=user_input, response_text=response_text)

if __name__ == '__main__':
    app.run(debug=True)
