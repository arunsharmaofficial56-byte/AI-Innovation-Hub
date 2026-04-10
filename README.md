# GuardianAI | Forensic News Analysis System 🛡️

GuardianAI is a professional-grade, AI-powered tool designed to detect misinformation and fabricated news patterns. By leveraging Advanced Natural Language Processing (NLP) and Machine Learning, it provides a forensic-level scan of news articles to ensure information integrity.

## 🚀 Key Features
- **Forensic Linguistic Scan**: Deep analysis of text patterns, token relations, and stylistic markers to identify non-veridical content.
- **Real-time Verification**: Instant classification of news as "Verified" or "Mistrusted" with high-fidelity accuracy.
- **Confidence Telemetry**: Visual probability scoring (Unreliability Index) to show the engine's certainty.
- **Guardian Dashboard**: A modern, glassmorphism-inspired interface built with Streamlit for a premium user experience.
- **Full-Stack ML Pipeline**: Complete pipeline from data preprocessing and TF-IDF vectorization to Logistic Regression classification.

## 🛠️ Technology Stack
- **Backend / ML**: Python, Scikit-Learn (Logistic Regression), NLTK, Pandas.
- **Preprocessing**: TF-IDF Vectorization, Regex-based cleaning.
- **Frontend**: Streamlit (with Custom CSS-in-JS styling).
- **Design**: Modern Glassmorphism, Google Fonts (Outfit & Inter).

## 📁 Project Structure
- `app.py`: The main logic for the professional GuardianAI web interface.
- `train_model.py`: Robust script for cleaning data, training the model, and saving engine weights.
- `Fake.csv` / `True.csv`: Datasets used for training (Standard news article format).
- `vectorizer.pkl` / `model.pkl`: Serialized model artifacts for production use.
- `metrics.pkl`: Performance tracking metadata.

## 🏃 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Model (Optional)
If you wish to retrain the engine with the provided datasets:
```bash
python train_model.py
```

### 3. Launch the Application
Start the professional dashboard:
```bash
streamlit run app.py
```

## 📄 Resume-Ready Description
> **GuardianAI Forensic System (NLP & Machine Learning)**
> - Engineered an AI-driven veracity analysis engine using Python and Scikit-Learn to detect misinformation in digital news.
> - Implemented a TF-IDF vectorization pipeline with custom linguistic preprocessing for high-accuracy text classification.
> - Developed a modern, glassmorphism-themed telemetry dashboard using Streamlit to visualize model confidence and article forensics.
> - Achieving rapid-response verification with a Logistic Regression backbone trained on standardized news datasets.

---
Developed with ❤️ by **Arun Sharma** | *Building the Future of Information Integrity.*
