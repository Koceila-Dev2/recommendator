from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from mistralai import Mistral

api_key = "MVSiHD2xUeCbEjWPPj43lUrwIReJsp4h"

# Initialisation de l'application Flask
app = Flask(__name__)

# Initialiser le client Mistral
client = Mistral(api_key= api_key)
model = "mistral-large-latest"



conversation_history = [
       {
        "role": "system",
        "content": (
            "You are a passionate cinephile and an expert film adviser. "
            "dans ta reponse tu va etre bref tu va rien dire apart me poser les questions "
            "les questions faut qu'elles soient pas trop technique et facile à repondre "
            "Your goal is to help users discover great movies based on their taste. "
            "You love discussing cinema, actors, directors, and different film genres. "
            "Tu vas poser les questions ( 5 au totale ) une par une dans le but de me proposer un film à la fin des 5 questions"
            "la finalitée c'est que tu me proposes un film au bout de ces 5 questions"
            "ecoutes bien et souviens toi de ce que je t'ai dis avant"
            
        )}
    
        ]


chat_response = client.chat.complete(
        model=model
        
        
        
       messages = conversation_history

    )

@app.route('/')
def index():
    return render_template('movie_finder.html')


@app.route('/generate', methods=['POST'])
def generate():
    
   
   
    chat_response = client.chat.complete(
        model=model,
        
        
        
       messages = conversation_history

    )
    
    response_text = chat_response.choices[0].message.content
    conversation_history.append({"role": "system", "content": response_text})
    user_input = request.form['prompt']
    conversation_history.append({"role": "user", "content": user_input})
    
    return render_template('movie_finder.html', user_input=user_input, response_text=response_text)

if __name__ == '__main__':
    app.run(debug=True)






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
