from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from mistralai import Mistral

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Initialisation de l'application Flask
app = Flask(__name__)

# Initialiser le client Mistral
client = Mistral(api_key="QQG84DG1tDMvuFN2lkOM9RqlGXOA6w11")
model = "mistral-large-latest"

@app.route('/')
def index():
    return render_template('movie_finder.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form['prompt']
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": user_input,
            },
        ]
    )
    response_text = chat_response.choices[0].message.content
    return render_template('movie_finder.html', user_input=user_input, response_text=response_text)

if __name__ == '__main__':
    app.run(debug=True)
