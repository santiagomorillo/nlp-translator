from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar CORS
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import os
import sentencepiece

# Crear la app de Flask
app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)

# Cargar el modelo
model_name = "Helsinki-NLP/opus-mt-en-fr"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# HTML como un string (lo puedes modificar)
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prueba de Servicio de Traducción de inglés a francés</title>
    <script>
        async function sendTranslation() {
            const text = document.getElementById("inputText").value;
            const response = await fetch("/translate", {  // Uso de ruta relativa
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: text })
            });
            const data = await response.json();
            document.getElementById("predictionResult").innerText = `Traducción: ${data.translation}`;
        }
    </script>
</head>
<body>
    <div style="max-width: 800px; margin: 0 auto; text-align: center;">
        <h1>Servicio de Traducción de inglés a francés</h1>
        <textarea id="inputText" rows="14" cols="100" placeholder="Escribe un texto en inglés para traducir a francés..."></textarea>
        <br><br>
        <button onclick="sendTranslation()">Obtener Traducción</button>
        <p id="predictionResult" style="margin-top: 20px; font-size: 18px; font-weight: bold;"></p>
    </div>
</body>
</html>
"""

# Ruta para servir el HTML
@app.route("/")
def home():
    print("Serving HTML content")
    return html_content

# Ruta para la predicción
@app.route("/translate", methods=["POST"])
def predict():
    data = request.json
    inputs = tokenizer(data["text"], return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model.generate(**inputs)  # Usa el método generate
        prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({"translation": prediction})

# Importante para Azure App Service - cambia la forma en que se ejecuta la app
if __name__ == '__main__':
    # Para desarrollo local
    app.run(port=80)
# else:
#     # Para producción en Azure
#     # Esta aplicación se ejecutará a través de Gunicorn
#     app.config['APPLICATION_ROOT'] = '/'