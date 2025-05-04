from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import tempfile
import os
from utils import extract_comments, extract_comments_from_url
from gemini_api import generate_kano_scores
from kano_fusion import classify_kano
from kano_plot import draw_custom_kano_plot
from email.message import EmailMessage
import smtplib
from io import BytesIO
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
CORS(app)  # Permet au React Frontend d'appeler le Backend

@app.route('/')
def home():
    return "API Kano Analysis is running ✅"

@app.route('/extract-comments', methods=['POST'])
def extract_comments_route():
    if 'file' in request.files:
        file = request.files['file']
        suffix = os.path.splitext(file.filename)[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            file.save(tmp.name)
            path = tmp.name
        
        comments = extract_comments(path, suffix)
        return jsonify({"comments": comments})
    
    elif 'url' in request.json:
        url = request.json['url']
        comments = extract_comments_from_url(url)
        return jsonify({"comments": comments})
    
    else:
        return jsonify({"error": "Aucun fichier ou URL fourni"}), 400

@app.route('/analyze-kano', methods=['POST'])
def analyze_kano_route():
    data = request.json
    comments = data.get('comments', [])

    if not comments:
        return jsonify({"error": "Liste de commentaires vide"}), 400

    kano_scores = generate_kano_scores(comments)
    if "error" in kano_scores:
        return jsonify({"error": kano_scores["error"]}), 500

    cs_plus = {k: v["cs+"] for k, v in kano_scores.items()}
    cs_minus = {k: v["cs-"] for k, v in kano_scores.items()}
    kano_result = classify_kano(cs_plus, cs_minus)

    return jsonify(kano_result)

@app.route('/generate-kano-plot', methods=['POST'])
def generate_plot_route():
    data = request.json
    if not data:
        return jsonify({"error": "JSON Kano non fourni"}), 400
    
    fig = draw_custom_kano_plot(data)

    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype='image/png')

@app.route('/api/analyze-file', methods=['POST'])
def analyze_file_route():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier fourni."}), 400

    file = request.files['file']
    suffix = os.path.splitext(file.filename)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        file.save(tmp.name)
        path = tmp.name

    # 📝 Extraction des commentaires
    comments = extract_comments(path, suffix)
    if not comments:
        return jsonify({"error": "Aucun commentaire extrait."}), 400

    # 🔥 Analyse Kano avec Gemini
    kano_scores = generate_kano_scores(comments)
    if "error" in kano_scores:
        return jsonify({"error": kano_scores["error"]}), 500

    # 📊 Classification
    cs_plus = {k: v["cs+"] for k, v in kano_scores.items()}
    cs_minus = {k: v["cs-"] for k, v in kano_scores.items()}
    kano_result = classify_kano(cs_plus, cs_minus)

    # 🎨 Générer le diagramme
    fig = draw_custom_kano_plot(kano_result)

    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    # 💾 Sauvegarder dans /static/kano_diagram.png
    output_path = os.path.join('static', 'kano_diagram.png')
    os.makedirs('static', exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(img_buffer.read())

    return jsonify({"diagram_url": "/static/kano_diagram.png"})


# ✅ 1️⃣ Fonction pour extraire les commentaires depuis l'URL
def extract_comments_from_url(url):
    """
    Extrait les commentaires d'une page HTML de manière robuste.
    """
    try:
        # Ajout du User-Agent dans les headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }

        # Effectuer la requête avec les headers
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Sélecteurs pour chercher les commentaires
        selectors = [
            '.review-text', '.comment-text', '.review-content',
            '.review-body', '.customer-review', '[class*=comment]', '[class*=review]'
        ]

        comments = []

        # 🔵 1. Chercher avec les sélecteurs standards
        for selector in selectors:
            for element in soup.select(selector):
                text = element.get_text(strip=True)
                if text and len(text) > 15:
                    comments.append(text)

        # 🔵 2. Si pas assez de commentaires, chercher dans toutes les balises <p> et <div> et <span>
        if len(comments) < 5:
            for p_tag in soup.find_all(['p', 'div', 'span']):
                text = p_tag.get_text(strip=True)
                if text and 20 < len(text) < 300:
                    comments.append(text)

        if not comments:
            raise Exception("No comments detected even after fallback extraction.")

        return comments

    except Exception as e:
        print(f"Erreur lors de l'extraction: {str(e)}")
        return []


# ✅ 2️⃣ Route API pour analyser une URL
@app.route('/api/analyze-url', methods=['POST'])
def analyze_url_route():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "Aucune URL fournie."}), 400

    try:
        # Extraction des commentaires
        comments = extract_comments_from_url(url)

        if not comments:
            return jsonify({"error": "Aucun commentaire trouvé."}), 400

        # 2️⃣ Analyse Kano avec Gemini
        kano_scores = generate_kano_scores(comments)
        if "error" in kano_scores:
            return jsonify({"error": kano_scores["error"]}), 500

        # 3️⃣ Classification Kano
        cs_plus = {k: v["cs+"] for k, v in kano_scores.items()}
        cs_minus = {k: v["cs-"] for k, v in kano_scores.items()}
        kano_result = classify_kano(cs_plus, cs_minus)

        # 4️⃣ Générer le diagramme
        fig = draw_custom_kano_plot(kano_result)

        img_buffer = BytesIO()
        fig.savefig(img_buffer, format='png')
        img_buffer.seek(0)

        # 5️⃣ Sauvegarde dans /static/kano_diagram.png
        output_path = os.path.join('static', 'kano_diagram.png')
        os.makedirs('static', exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(img_buffer.read())

        return jsonify({"diagram_url": "/static/kano_diagram.png"})

    except Exception as e:
        print(f"Erreur dans analyze_url_route: {str(e)}")
        return jsonify({"error": f"Erreur lors de l'analyse de l'URL : {str(e)}"}), 500


# Configuration SMTP
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
EMAIL_ADDRESS = 'aminamegzari13@gmail.com'         # ✅ Ton adresse Gmail
EMAIL_PASSWORD = 'algw visw rzwg zgrl'     # ✅ Mot de passe d'application Gmail

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    print("📩 Email reçu :", data)
    recipient_email = data.get('email')
    diagram_url = data.get("diagram_url")


    if not recipient_email or not diagram_url:
        return {"error": "Missing email or diagram URL"}, 400


    image_path = os.path.join("static", "kano_diagram.png")
    if not os.path.exists(image_path):
        return jsonify({'error': 'Le fichier kano_diagram.png est introuvable.'}), 404

    try:
        msg = EmailMessage()
        msg['Subject'] = 'Votre Diagramme Kano'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_email
        msg.set_content("Bonjour,\n\nVoici votre diagramme Kano généré automatiquement en pièce jointe.")

        with open(image_path, 'rb') as f:
            img_data = f.read()
        msg.add_attachment(img_data, maintype='image', subtype='png', filename='kano_diagram.png')

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        return jsonify({'message': 'Email envoyé avec succès !'}), 200
    except Exception as e:
        print("❌ ERREUR SMTP :", str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/download-diagram')
def download_diagram():
    return send_from_directory(
        directory='static',
        path='kano_diagram.png',
        as_attachment=True
    )

# ✅ 3️⃣ Lancement du serveur
if __name__ == '__main__':
    app.run(debug=True) 