### 🚀 LinkedIn Post Generator (LLM-powered)

This project helps users generate tailored LinkedIn posts based on topic, tone, and language preferences using LLM (Groq LLaMA 3) and Streamlit.

---

##E 📁 Project Structure

├── data/
│ ├── raw_posts.json # Original input posts
│ └── processed_posts.json # Posts enriched with metadata
├── few_shot.py # Few-shot example retriever
├── generate.py # Post generation logic
├── llm_helper.py # LLM configuration
├── post_generator.py # Prompt + LLM invocation
├── processor.py # Metadata extractor & tag unifier
├── app.py # Streamlit UI
├── .env # API key (not pushed to GitHub)
├── requirements.txt # Python dependencies
└── README.md # You're here!


---

### ⚙️ Setup Instructions

## 1. **Clone the Repository**
```bash```
git clone https://github.com/Prabalt22/AI-Learning/linkedin-post-generator.git
cd linkedin-post-generator

## Create and Activate a Virtual Environment
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

## Install Dependencies
pip install -r requirements.txt

## Set Up Environment Variables
Create a .env file in the root directory: GROQ_API_KEY=your_groq_api_key_here

## Preprocess Data
Before running the app, enrich your raw_posts.json: python processor.py
This will generate a processed_posts.json in data/.

## Run the App
streamlit run app.py

---

### ✍️ Features
  🎯 Topic-specific LinkedIn post generation
  📏 Choose post length (Short / Medium / Long)
  🌐 Supports English & Hinglish
  🤖 LLM-powered personalization using Groq LLaMA-3

---

