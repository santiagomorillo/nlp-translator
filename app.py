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
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <script>
        async function sendTranslation() {
            const translateButton = document.getElementById("translateButton");
            const clearButton = document.getElementById("clearButton");
            const spinner = document.getElementById("spinner");
            translateButton.disabled = true;
            clearButton.disabled = true;
            spinner.style.display = "inline-block";
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
            translateButton.disabled = false;
            clearButton.disabled = false;
            spinner.style.display = "none";
        }

        function clearText() {
            document.getElementById("inputText").value = "";
            document.getElementById("predictionResult").innerText = "";
        }
    </script>
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <h1 class="text-center">Servicio de Traducción de inglés a francés</h1>
                <div class="form-group">
                    <textarea id="inputText" class="form-control" rows="10" placeholder="Escribe un texto en inglés para traducir a francés..."></textarea>
                </div>
                <div class="text-center">
                    <button id="translateButton" class="btn btn-primary btn-lg" onclick="sendTranslation()">Obtener Traducción</button>
                    <button id="clearButton" class="btn btn-secondary btn-lg ml-2" onclick="clearText()">Nueva Traducción</button>
                    <div id="spinner" class="spinner-border text-primary ml-3" role="status" style="display: none;">
                        <span class="sr-only">Loading...</span>
                    </div>
                </div>
                <p id="predictionResult" class="mt-4 text-center font-weight-bold"></p>
            </div>
        </div>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
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