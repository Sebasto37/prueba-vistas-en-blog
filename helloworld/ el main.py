from flask import Flask, request, render_template_string
import requests
import openai
import os
import base64
from collections import Counter
import re

app = Flask(__name__)

# ----------- Función para extraer palabras clave ----------- #
def extract_keywords(titles):
    words = []
    for title in titles:
        # Remover caracteres especiales y dividir en palabras
        tokens = re.findall(r'\b\w+\b', title.lower())
        words.extend(tokens)
    
    # Lista de palabras vacías comunes en español
    stop_words = set([
        "a", "de", "en", "y", "el", "la", "los", "las", 
        "un", "una", "unos", "unas", "del", "al", "que", "por"
    ])
    
    # Contar frecuencia de palabras ignorando stopwords
    keyword_counts = Counter(word for word in words if word not in stop_words)
    
    return keyword_counts.most_common(10)  # Top 10 palabras más comunes


# ----------- Plantilla HTML ----------- #
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>SEO App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #2c3e50; }
        .result { background: #f4f4f4; padding: 10px; margin: 10px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Analizador SEO</h1>
    <form method="POST">
        <label>Ingresa títulos de páginas (uno por línea):</label><br><br>
        <textarea name="titles" rows="6" cols="60"></textarea><br><br>
        <button type="submit">Analizar</button>
    </form>

    {% if keywords %}
    <h2>Palabras clave más comunes</h2>
    <div>
        {% for word, count in keywords %}
            <div class="result">{{ word }} - {{ count }}</div>
        {% endfor %}
    </div>
    {% endif %}
</body>
</html>
'''


# ----------- Ruta principal ----------- #
@app.route("/", methods=["GET", "POST"])
def home():
    keywords = None
    if request.method == "POST":
        titles_input = request.form["titles"].split("\n")
        keywords = extract_keywords(titles_input)
    return render_template_string(HTML_TEMPLATE, keywords=keywords)


# ----------- Punto de entrada ----------- #
if __name__ == "__main__":
    app.run(debug=True)
