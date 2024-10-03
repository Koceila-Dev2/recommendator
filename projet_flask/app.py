from flask import Flask, render_template, request, session
from dotenv import load_dotenv
import os
from mistralai import Mistral

load_dotenv()
api_key = os.getenv("API_KEY")

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")  # Clé pour la session

# Initialiser le client Mistral
client = Mistral(api_key=api_key)
model = "mistral-large-latest"

@app.route('/')
def index():
    return render_template('movie_finder.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form['prompt']

    # Si l'historique n'existe pas dans la session, initialiser
    if 'conversation_history' not in session:
        session['conversation_history'] = [
            {
                "role": "system",
                "content": (
                "You are a passionate cinephile and an expert film adviser. "
                "dans ta reponse tu va etre bref tu va rien dire apart me poser les 5 questions "
                "les questions faut qu'elles soient pas trop technique et facile à repondre "
                "Your goal is to help users discover great movies based on their taste. "
                "tu va commencer quand je te dis 'salut' et tu commencera par un epetite presentation de toi. Tu vas poser les questions une par une dans le but de me proposer un film."
                )
            }
        ]

    # Ajouter l'input utilisateur à l'historique
    conversation_history = session['conversation_history']
    conversation_history.append({"role": "user", "content": user_input})

    # Générer la réponse du modèle
    chat_response = client.chat.complete(
        model=model,
        messages=conversation_history
    )

    # Ajouter la réponse du bot à l'historique
    response_text = chat_response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": response_text})

    # Sauvegarder l'historique dans la session
    session['conversation_history'] = conversation_history

    # Vérifier si 5 questions ont été posées par l'utilisateur
    # if len([msg for msg in conversation_history if msg['role'] == 'user']) >= 5:
    #     # Réinitialiser après la recommandation finale
    #     session.pop('conversation_history', None)
    if len([msg for msg in conversation_history if msg['role'] == 'user']) >= 7:
        # Réinitialiser après la recommandation finale
        session.pop('conversation_history', None)

    return render_template('movie_finder.html', user_input=user_input, response_text=response_text)

if __name__ == '__main__':
    app.run(debug=True)



# @app.route('/generate', methods=['POST'])
# def generate():
    
   
   
#     chat_response = client.chat.complete(
#         model=model,
        
        
        
#        messages = conversation_history

#     )
    
#     response_text = chat_response.choices[0].message.content
#     conversation_history.append({"role": "system", "content": response_text})
#     user_input = request.form['prompt']
#     conversation_history.append({"role": "user", "content": user_input})
    
#     return render_template('movie_finder.html', user_input=user_input, response_text=response_text)








# conversation_history = [
#     {
#         "role": "system",
#         "content": (
#             "You are a passionate cinephile and an expert film adviser. "
#             "dans ta reponse tu va etre bref tu va rien dire apart me poser les 5 questions "
#             "les questions faut qu'elles soient pas trop technique et facile à repondre "
#             "Your goal is to help users discover great movies based on their taste. "
#             "You love discussing cinema, actors, directors, and different film genres. "
#             "Tu vas poser les questions une par une dans le but de me proposer un film."
#         ),
#     }
# ]

# # Le chatbot va poser 5 questions une par une
# num_questions = 5
# for i in range(num_questions):
#     # Demander au modèle de générer la prochaine question
#     chat_response = client.chat.complete(
#         model=model,
#         messages=conversation_history
#     )
    
#     # Obtenir la question du modèle
#     question = chat_response.choices[0].message.content
#     print(f"Question {i+1}: {question}")

#     # Obtenir la réponse de l'utilisateur
#     user_response = input("Votre réponse: ")

#     # Ajouter la question et la réponse dans l'historique
#     conversation_history.append({"role": "assistant", "content": question})
#     conversation_history.append({"role": "user", "content": user_response})

# print("\nMerci pour vos réponses ! Je vais maintenant vous recommander un film...")

# # Une fois les 5 questions posées, le bot pourrait analyser les réponses pour recommander un film
# # (Cette partie est à implémenter selon tes besoins)

# if __name__ == "__main__":
#     ask_question()
