from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv
import os
from mistralai import Mistral

app = Flask(__name__)
load_dotenv()
model = "mistral-large-latest"
client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', response=None)

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form.get('user_input', '')
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": user_input,
            },
        ]
    )
    
    # Vérifiez si la réponse a bien été obtenue
    response_message = chat_response.choices[0].message.content if chat_response.choices else "Aucune réponse obtenue."
    return render_template('index.html', response=response_message)  # Renvoie la réponse à la page d'accueil

if __name__ == '__main__':
    app.run(debug=True)
