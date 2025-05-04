# Kano LLM Generator



> Visualize what truly matters to your customers with minimal effort.

---

##  Overview

**Kano LLM Generator** is an AI-powered web platform that simplifies customer feedback analysis using Large Language Models (LLMs). The tool helps product teams classify customer needs into Kano categories (Basic, Performance, Excitement, etc.) and instantly generate Kano diagrams.

---

##  Features

- ✅ **File Upload Support**: Upload customer feedback through:
  - `.csv` files
  - `.xlsx` Excel files
  - `.txt` files

- 🔗 **URL Import**: Automatically scrape customer feedback from a given website URL using our web scraping pipeline.

-  **LLM-Powered Classification**:
  - Sentiment analysis (positive/negative)
  - LLM-based categorization of feedback into Kano classes

- 📈 **Automatic Kano Diagram Generation**:
  - Real-time chart rendering based on processed feedback
  - Clear visualization of feature classification

- **Export & Delivery**:
  - Download the Kano diagram as an image (`.png`)
  - Optionally receive the diagram by email

---

##  Pipelines Overview

### 1. File/URL Intake
- Files and URLs are processed via secure Flask backend endpoints.
- Validation ensures format correctness and cleans data.

### 2. Data Preprocessing
- Cleans feedback text (stop words removal, stemming, etc.)
- Detects and filters out empty or irrelevant entries

### 3. Sentiment Analysis
- Classifies feedback into **positive** or **negative** using a fine-tuned model

### 4. Kano Classification via LLM
- Uses a pre-configured LLM (e.g. Mistral via Ollama) to tag each comment as:
  - **Must-be**
  - **Attractive**
  - **One-dimensional**
  - **Indifferent**
  - **Reverse**

### 5. Diagram Generation
- Aggregates and visualizes results using Plotly or Matplotlib
- Provides downloadable Kano chart

### 6. Email Dispatch (Optional)
- Sends the generated chart as an email attachment using SMTP or SendGrid API

---

##  Tech Stack

| Layer             | Tools/Libraries                    |
|------------------|------------------------------------|
| Frontend         | React.js, Tailwind CSS             |
| Backend          | Flask, Python                      |
| LLM Integration  | Gemini               |
| Web Scraping     | BeautifulSoup, Requests            |
| Data Processing  | Pandas, NumPy                      |
| Emailing         | Flask-Mail, SendGrid               |
| Deployment       |Github     |Git

---

##  How to Use

1. Launch the platform or run locally.
2. Upload a feedback file or input a URL.
3. Choose your settings and click "Generate".
4. View or download your Kano diagram.
5. (Optional) Enter an email to receive it automatically.

---

##  Contact

If you’d like to collaborate, contribute, or ask questions:

- 💼 GitHub: [BELEMDIOUIraja](https://github.com/BELEMDIOUIraja)
-  [Amina Magzari](https://github.com/aminamegzari1)
  

-
