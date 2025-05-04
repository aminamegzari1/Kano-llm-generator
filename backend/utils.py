import pandas as pd
import fitz
from docx import Document
import os
import re
import streamlit as st
import requests
from bs4 import BeautifulSoup


def extract_comments_from_pdf(path):
    with fitz.open(path) as doc:
        text = "\n".join(page.get_text() for page in doc)

    raw_lines = text.splitlines()
    cleaned_lines = [line.strip() for line in raw_lines if line.strip()]
    merged_comments = merge_multiline_comments(cleaned_lines)
    return merged_comments

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

def extract_comments(file_path, extension):
    comments = []

    if extension == '.csv':
        try:
            df = pd.read_csv(file_path)

            # Cherche automatiquement la première colonne de texte
            text_columns = [col for col in df.columns if df[col].dtype == 'object']

            if text_columns:
                selected_column = text_columns[0]  # Prendre la première colonne texte trouvée
                comments = df[selected_column].dropna().apply(clean_text).tolist()
            else:
                # fallback : si aucune colonne texte trouvée
                comments = df.iloc[:, 0].dropna().astype(str).apply(clean_text).tolist()

        except Exception as e:
            print(f"Erreur lors de la lecture du fichier CSV : {e}")
            return []

    elif extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            comments = [clean_text(line) for line in f.readlines() if line.strip()]

    elif extension == '.pdf':
        comments = extract_comments_from_pdf(file_path)

    elif extension == '.docx':
        doc = Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
        comments = [clean_text(c) for c in text.split('\n') if c.strip()]

    else:
        raise ValueError("Format non supporté.")

    return comments

def merge_multiline_comments(lines):
    comments = []
    current = ""

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Si ligne commence par une majuscule ou chiffre, considère que c'est un nouveau commentaire
        if re.match(r"^[A-Z0-9]", line) and current:
            comments.append(current.strip())
            current = line
        else:
            current += " " + line

    if current:
        comments.append(current.strip())

    return comments
#extraction de l' URL
def extract_comments_from_url(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Erreur HTTP lors de la requête : {e}")
    soup = BeautifulSoup(response.content, "html.parser")

    # 🔍 Personnalise ce sélecteur selon le site ciblé
    possible_classes = ["comment", "review", "user-comment", "feedback", "review-content"]
    comments = []

    for class_name in possible_classes:
        elements = soup.find_all(class_=class_name)
        for el in elements:
            text = el.get_text(strip=True)
            if text and len(text) > 20:
                cleaned = clean_review_text(text)
                if cleaned:
                    comments.append(cleaned)


    if not comments:
        raise ValueError("Aucun commentaire détecté avec les sélecteurs standards.")

    return comments


def clean_review_text(text):
    # Supprimer les évaluations de type "5.0 out of 5 stars"
    text = re.sub(r"\b\d+(\.\d+)? out of 5 stars\b", "", text, flags=re.IGNORECASE)

    # Supprimer "Reviewed in ... on [date]"
    text = re.sub(r"Reviewed in .*? on \w+ \d{1,2}, \d{4}", "", text, flags=re.IGNORECASE)

    # Supprimer "Style: ...", "Verified Purchase", "Read more", "Helpful", "Report"
    text = re.sub(r"Style:.*?(?=(This|It|They|Read|I|Works|Works|No|Ok|Problem|⭐|★|[A-Z]))", "", text)
    text = re.sub(r"(Verified Purchase|Helpful|Read more|Report|\d+ people found this helpful)", "", text, flags=re.IGNORECASE)

    # Supprimer les emojis étoiles
    text = re.sub(r"[⭐★]+", "", text)

    # Supprimer le nom au début (ex: "Eric Nordseth" ou "Pmb")
    text = re.sub(r"^[A-Z][a-z]+\s?[A-Z]?[a-z]*", "", text)

    # Nettoyage final
    text = re.sub(r"\s+", " ", text).strip()
    return text
