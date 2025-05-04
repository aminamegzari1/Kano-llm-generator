import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re



load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def safe_extract_json(text):
    # Supprimer les balises Markdown ```json ou ```
    text = re.sub(r"```json|```", "", text).strip()

    # Chercher le premier bloc JSON qui commence par { et finit par }
    json_start = text.find('{')
    json_end = text.rfind('}') + 1  # inclure la dernière accolade

    if json_start == -1 or json_end == -1:
        return None, "❌ Aucun bloc JSON trouvé dans la réponse."

    clean_json = text[json_start:json_end]

    try:
        parsed = json.loads(clean_json)
        return parsed, None
    except json.JSONDecodeError as e:
        return None, f"❌ Erreur de parsing JSON : {e}"
def generate_kano_scores(comments):
    prompt = "Voici une liste de commentaires clients :\n\n"
    for i, comment in enumerate(comments):
        prompt += f"{i+1}. {comment}\n"

    prompt += """
1. **Identifier les aspects** les plus importants du produit cités dans les commentaires (maximum 15, ne garde que les plus récurrents et pertinents).
2. **Regroupe les synonymes** et variantes (ex : “autonomie”, “durée de la batterie” → “Autonomie de la batterie”).
3. **Ignore les éléments flous ou peu exploitables** (ex : “bon produit”, “satisfait”, “j’aime bien”, etc.).
4. Pour chaque aspect retenu, compte :
   - Le nombre de commentaires exprimant une **satisfaction claire** (cs+)
   - Le nombre exprimant une **insatisfaction ou frustration claire** (cs-)
5. Calcule pour chaque aspect :
   - `cs+` = satisfaction_count / total_comments
   - `cs-` = insatisfaction_count / total_comments
   - Limite les scores entre 0 et 1 avec deux décimales
6. Applique une **catégorisation stricte** selon le modèle Kano :
   - Must-be (faible cs+, fort cs-)
   - Attractive (fort cs+, faible cs-)
   - One-dimensional (forts cs+ et cs-)
   - Indifferent (faibles cs+ et cs-)

⚠️ Le JSON final doit être **propre**, **exploitable directement**, et au format suivant :

```json
{
  "Autonomie de la batterie": { "cs+": 0.24, "cs-": 0.02, "category": "Attractive" },
  "Clavier": { "cs+": 0.14, "cs-": 0.16, "category": "One-dimensional" },
  "Caméra": { "cs+": 0.05, "cs-": 0.28, "category": "Must-be" }
}


"""

    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        raw = response.text.strip()

      
        # ✅ Extraction robuste du premier JSON trouvé
        json_match = re.search(r'(\{(?:.|\n)*?\})', raw)
        if not json_match:
            return {"error": "Aucun bloc JSON trouvé dans la réponse de Gemini."}

        clean_json = json_match.group(1)

        # ✅ Conversion en dictionnaire Python
        parsed, error = safe_extract_json(raw)
        if error:
            return {"error": error}
        return parsed

    except Exception as e:
        return {"error": str(e)}