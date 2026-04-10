import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
import os

# Download stopwords if not already present
nltk.download('stopwords')

def preprocess_text(text):
    text = str(text).lower() # Convert to lowercase
    text = re.sub('\[.*?\]', '', text) # Remove text in brackets
    text = re.sub("\\W"," ",text) # Remove special characters
    text = re.sub('https?://\S+|www\.\S+', '', text) # Remove URLs
    text = re.sub('<.*?>+', '', text) # Remove HTML tags
    text = re.sub('\n', '', text) # Remove newlines
    text = re.sub('\w*\d\w*', '', text) # Remove words containing numbers
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text

def train_model():
    print("-" * 50)
    print("GuardianAI: Training Detection Engine")
    print("-" * 50)
    
    # Define file paths
    fake_path = 'Fake.csv'
    true_path = 'True.csv'
    
    if not os.path.exists(fake_path) or not os.path.exists(true_path):
        print(f"Error: Datasets '{fake_path}' or '{true_path}' not found.")
        print("Suggestion: Generate or download 'Fake.csv' and 'True.csv' first.")
        return

    print("Loading datasets...")
    df_fake = pd.read_csv(fake_path)
    df_true = pd.read_csv(true_path)

    # Validate columns
    required_cols = ['text']
    for col in required_cols:
        if col not in df_fake.columns or col not in df_true.columns:
            print(f"Error: Required column '{col}' missing from CSV files.")
            return

    # Labeling
    df_fake["class"] = 0
    df_true["class"] = 1

    df = pd.concat([df_fake, df_true], axis=0)
    
    # Text-only selection
    if 'title' in df.columns:
        df['text'] = df['title'].fillna('') + " " + df['text'].fillna('')

    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    print("Preprocessing data (cleaning linguistic markers)...")
    df['text'] = df['text'].apply(preprocess_text)

    # Model Pipeline
    x = df['text']
    y = df['class']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    print("Vectorizing text using TF-IDF...")
    vectorization = TfidfVectorizer()
    xv_train = vectorization.fit_transform(x_train)
    xv_test = vectorization.transform(x_test)

    print("Training Logistic Regression Model...")
    model = LogisticRegression(max_iter=1000)
    model.fit(xv_train, y_train)

    # Metrics
    pred = model.predict(xv_test)
    acc = accuracy_score(y_test, pred)
    print(f"Training Complete! Testing Accuracy: {acc*100:.2f}%")

    # Save artifacts
    print("Saving engine weights to disk...")
    
    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorization, f)
        
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    with open('metrics.pkl', 'wb') as f:
        pickle.dump({'accuracy': acc}, f)
        
    print("-" * 50)
    print("System Ready. Run 'streamlit run app.py' to launch.")
    print("-" * 50)

if __name__ == "__main__":
    train_model()
