# Student Performance Predictor 🎓📈

Student Performance Predictor is an end-to-end Machine Learning web application designed to forecast a student's final exam score based on their academic and lifestyle habits. It leverages a robust regression pipeline to provide data-driven insights for educators and students.

## 🚀 Key Features
- **Predictive Scoring**: Estimate final exam marks using input parameters like Study Hours, Attendance, and Previous Performance.
- **Lifestyle Impact Analysis**: Factors in Sleep Hours, Internet Usage, and Extracurricular Activities to provide a holistic prediction.
- **Automated ML Pipeline**: Implements a Scikit-Learn Pipeline that handles Feature Scaling (Standardization) and Categorical Encoding (One-Hot) seamlessly.
- **Random Forest Backbone**: Driven by a Random Forest Regressor for superior non-linear pattern recognition.
- **Interactive Dashboard**: Polished Streamlit UI for real-time adjustments and instant predictions.

## 🛠️ Technology Stack
- **Machine Learning**: Python, Scikit-Learn (Random Forest), NumPy, Pandas.
- **Preprocessing**: Pipeline architecture with ColumnTransformer (StandardScaler & OneHotEncoder).
- **Frontend**: Streamlit.
- **Serialization**: Pickle for model persistence.

## 📁 Project Structure
- `app.py`: Streamlit application for the interactive web interface.
- `train_model.py`: Training script for data generation, preprocessing, and model fitting.
- `student_data.csv`: The synthetic high-quality dataset used for the model.
- `model_pipeline.pkl`: The serialized Scikit-Learn pipeline (Preprocessing + Regressor).
- `metrics.pkl`: Accuracy metrics (R² score).

## 🏃 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train and Generate Model
```bash
python train_model.py
```

### 3. Launch App
```bash
streamlit run app.py
```

## 📄 Resume-Ready Description
> **Student Academic Performance Forecaster (Machine Learning)**
> - Developed a predictive analytics platform using Python and Random Forest Regression to estimate student exam scores with high precision (R² Score).
> - Engineered an automated Scikit-Learn pipeline to handle complex preprocessing, including feature scaling and categorical encoding of lifestyle data.
> - Built a real-time interactive dashboard in Streamlit to allow users to visualize the impact of behavioral variables on academic outcomes.
> - Optimized model performance through tree-based ensemble methods and robust data normalization.

---
Developed with ❤️ by **Arun Sharma** | *Empowering Education through Data Science.*
