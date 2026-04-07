# 🌿 LeafAI — Plant Disease Detection

An AI-powered web application that detects plant leaf diseases from photos using deep learning.

## Features

- 📷 Upload a leaf image or capture one using your camera
- 🧠 AI model identifies the disease with a confidence score
- 💊 Shows cause and treatment for the detected disease
- 🌱 Covers 14 plant types and 38 disease classes

## Project Structure

```
LeafAI/
├── app.py                        # Flask backend + ML model integration
├── plant_disease.json            # Disease info (name, cause, treatment)
├── models/                       # Trained Keras model
├── requirements.txt              # Python dependencies
├── templates/
│   ├── base.html                 # Shared navbar, footer, layout
│   ├── home.html                 # Landing page
│   ├── predict.html              # Prediction page (upload + camera)
│   └── coverage.html            # Supported plants overview
└── static/
    ├── css/
    │   ├── style_pages.css       # Base styles, navbar, home, coverage
    │   └── style_predict.css     # Predict page, result panel, animations
    └── js/
        ├── script_pages.js       # Upload, drag-drop, tab switching
        └── script_predict.js     # Camera capture, spinner, confidence bar
```

## How to Run

1. Clone the repository:
```bash
git clone https://github.com/YourUsername/LeafAI.git
cd LeafAI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Add your trained model to the `models/` folder as `plant_disease_model.keras`

4. Run the app:
```bash
python app.py
```

5. Open your browser and go to `http://localhost:5000`

## Tech Stack

- **Backend:** Python, Flask, TensorFlow/Keras
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Model:** CNN with transfer learning (PlantVillage dataset)
- **Dataset:** 14 plant species, 39 disease classes

## Team

- Member 1 — Backend, ML model, predict page, animations
- Member 2 — Frontend pages, coverage page, UI styles
