// frontend/src/api.js
import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000';

export const extractComments = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await axios.post(`${API_URL}/extract-comments`, formData);
    return res.data;
  } catch (err) {
    console.error("Erreur d'extraction des commentaires :", err);
  }
};

export const analyzeKano = async (comments) => {
  try {
    const res = await axios.post(`${API_URL}/analyze-kano`, { comments });
    return res.data;
  } catch (err) {
    console.error("Erreur d'analyse Kano :", err);
  }
};

export const generateKanoPlot = async (kanoData) => {
  try {
    const res = await axios.post(`${API_URL}/generate-kano-plot`, kanoData, { responseType: 'blob' });
    const url = URL.createObjectURL(new Blob([res.data]));
    return url;
  } catch (err) {
    console.error("Erreur de génération du diagramme Kano :", err);
  }
};
