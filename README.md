# 🌿 LeafAI

### Plant Disease Detection System

**Upload a leaf photo or use your camera — get an AI diagnosis in under 2 seconds.**
 
## 📌 Overview

LeafAI is a full-stack web application that uses a **Convolutional Neural Network (CNN)** trained on the [PlantVillage dataset](https://www.tensorflow.org/datasets/catalog/plant_village) to diagnose plant diseases from photographs. Users can upload a leaf image or capture one directly from their device camera. The system returns:

- ✅ Disease name (human-readable)
- 📊 Confidence percentage with animated bar
- 🦠 Cause of the disease
- 💊 Recommended treatment

> Built as a Software Engineering project by **Team GreenByte** — 2 members, clean role separation, no Bootstrap, pure custom CSS.

---

## 🖼️ Screenshots

| Home Page | Predict Page | Result |
|-----------|-------------|--------|
| Hero section with CTA | Upload / Camera tabs | Disease + confidence + treatment |

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📁 **Image Upload** | Drag-and-drop or file browser — PNG, JPG supported |
| 📷 **Live Camera** | Capture directly from device camera (rear-facing on mobile) |
| 🧠 **AI Prediction** | CNN classifies 38 disease classes across 14 plant species |
| 📊 **Confidence Bar** | Animated bar with counter — High / Moderate / Low tier labels |
| 🦠 **Cause & Treatment** | Disease cause and recommended cure shown after every prediction |
| 🌱 **Coverage Page** | Browse all 14 supported plants and their detectable diseases |
| 🔧 **Debug Endpoint** | `/debug` — inspect raw model probabilities for troubleshooting |
| ⚡ **Fast** | Results in under 2 seconds on a standard server |

---

## 🛠️ Tech Stack

### Backend
| Tool | Purpose |
|------|---------|
| **Python 3.10+** | Server-side language |
| **Flask 3.0** | Web framework — routing, templates, request handling |
| **TensorFlow / Keras** | Deep learning model loading and inference |
| **NumPy** | Array operations — `argmax`, `expand_dims`, preprocessing |
| **UUID** | Unique filename generation for uploads |
| **Base64** | Camera capture encoding/decoding |

### Frontend
| Tool | Purpose |
|------|---------|
| **HTML5 + Jinja2** | Templating — Flask fills `{{ }}` tags server-side |
| **CSS3** | Custom botanical dark theme — no Bootstrap |
| **Vanilla JavaScript** | Camera, drag-drop, spinner, reveal animations, confidence counter |

### Machine Learning
| Detail | Value |
|--------|-------|
| **Architecture** | CNN with transfer learning (auto-detected backbone) |
| **Dataset** | PlantVillage — 87,000+ images |
| **Classes** | 38 (14 plant species × diseases + healthy) |
| **Input** | Auto-read from model — typically 224×224 or 160×160 px |
| **Preprocessing** | Auto-detected: MobileNet / EfficientNet / ResNet / Inception / ÷255 |

---

## 📁 Project Structure

```
LeafAI/
│
├── app.py                        # Flask backend — all routes & ML logic
├── plant_disease.json            # Disease info — 38 entries (name, cause, cure)
├── requirements.txt              # Python dependencies
├── .gitignore                    # Excludes model, uploads, pycache
│
├── models/
│   └── plant_disease_model.keras # Trained CNN model (add your own)
│
├── uploadimages/                 # Saved uploads — auto-created at runtime
│
├── templates/
│   ├── base.html                 # Shared navbar, footer, loads CSS & JS
│   ├── home.html                 # Landing page
│   ├── predict.html              # Predict form + result display
│   └── coverage.html            # All supported plants & diseases
│
└── static/
    ├── css/
    │   ├── style_pages.css       # Variables, navbar, home, coverage styles
    │   └── style_predict.css     # Predict page, result panel, animations
    └── js/
        ├── script_pages.js       # Upload, drag-drop, tab switching
        └── script_predict.js     # Camera, spinner, confidence animation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip
- A trained `.keras` model file (PlantVillage CNN)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/YourUsername/LeafAI.git
cd LeafAI
```

**2. Create a virtual environment (recommended)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your trained model**

Place your trained Keras model in the `models/` folder:
```
models/plant_disease_model.keras
```

> The app auto-reads the model's input shape and detects the preprocessing backbone — no manual configuration needed.

**5. Run the app**
```bash
python app.py
```

**6. Open your browser**
```
http://localhost:5000
```

---

## 🌿 Supported Plants & Diseases

The model covers **38 classes** across **14 plant species**:

| Plant | Diseases Covered |
|-------|-----------------|
| 🍎 Apple | Apple scab, Black rot, Cedar rust, Healthy |
| 🫐 Blueberry | Healthy |
| 🍒 Cherry | Powdery mildew, Healthy |
| 🌽 Corn | Grey leaf spot, Common rust, Northern blight, Healthy |
| 🍇 Grape | Black rot, Esca, Leaf blight, Healthy |
| 🍊 Orange | Citrus greening (HLB) |
| 🍑 Peach | Bacterial spot, Healthy |
| 🌶️ Pepper | Bacterial spot, Healthy |
| 🥔 Potato | Early blight, Late blight, Healthy |
| 🍓 Strawberry | Leaf scorch, Healthy |
| 🍅 Tomato | Bacterial spot, Early blight, Late blight, Leaf mold, Septoria, Spider mites, Target spot, Yellow leaf curl virus, Mosaic virus, Healthy |
| 🫑 Squash | Powdery mildew |
| 🫘 Soybean | Healthy |
| 🌿 Raspberry | Healthy |

> Visit `/coverage` in the app for the complete interactive list.

---

## 🔌 API Routes

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/` | Home page |
| `GET` | `/coverage` | Disease coverage overview |
| `GET` | `/predict` | Predict form (empty) |
| `POST` | `/predict` | Submit image → run model → return results |
| `GET/POST` | `/debug` | Diagnostic tool — raw probabilities for all 38 classes |
| `GET` | `/uploadimages/<filename>` | Serve uploaded image files |

### POST `/predict` — Accepted Inputs

**File upload** (multipart form):
```
Content-Type: multipart/form-data
Field: image (file)
```

**Camera capture** (base64):
```
Content-Type: application/x-www-form-urlencoded
Field: captured_image = "data:image/jpeg;base64,/9j/4AAQ..."
```

---

## 🔧 Debug Tool

If the model always predicts the same class, visit the debug endpoint:

```
http://localhost:5000/debug
```

Upload any leaf image. The response JSON tells you:

```json
{
  "model_input_size": "224x224",
  "preprocess_mode": "mobilenet",
  "num_classes_model": 39,
  "num_classes_json": 39,
  "top_5_predictions": [
    { "rank": 1, "index": 26, "name": "Tomato___Late_blight", "probability": 94.32 },
    { "rank": 2, "index": 25, "name": "Tomato___Leaf_Mold",   "probability":  3.11 }
  ]
}
```

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| One class always 99%+ | Preprocessing mismatch | Check `PREPROCESS_MODE` in `app.py` |
| All classes ~2.6% (flat) | Wrong normalization | Override `PREPROCESS_MODE = 'divide255'` |
| Top class name is wrong | JSON order mismatch | Reorder `plant_disease.json` to match training class indices |
| `FileNotFoundError` on model | Model not in `models/` | Add `plant_disease_model.keras` to `models/` |

---

## 📐 Architecture

```
Browser
  │
  ├─ GET /predict ──────────────────► Flask predict()
  │                                       │ render predict.html (empty form)
  │◄────────────────────────────────────── │
  │
  ├─ POST /predict (image data) ───► Flask predict()
  │                                       │
  │                                       ├─ Save image (UUID filename)
  │                                       │
  │                                       ├─ extract_features()
  │                                       │    ├─ load_img()  → PIL Image
  │                                       │    ├─ img_to_array() → (H,W,3)
  │                                       │    ├─ preprocess_input() → normalized
  │                                       │    └─ expand_dims() → (1,H,W,3)
  │                                       │
  │                                       ├─ model.predict() → (1,38) probs
  │                                       │
  │                                       ├─ argmax → pred_index
  │                                       ├─ max    → confidence %
  │                                       └─ plant_disease[pred_index] → disease info
  │
  │◄──── render predict.html (results) ───────────────────────────────
  │
  └─ DOMContentLoaded (JS)
       ├─ Stagger .reveal-item animations
       ├─ Animate confidence bar (CSS transition)
       └─ countUp() → 0% → actual % (requestAnimationFrame)
```

---

## 👥 Team

**Team GreenByte**

| Member | Role | Files Owned |
|--------|------|-------------|
| **Member 1** | Backend · ML · Predict Page | `app.py`, `predict.html`, `style_predict.css`, `script_predict.js`, `plant_disease.json`, `models/` |
| **Member 2** | Frontend · Templates · UI | `base.html`, `home.html`, `coverage.html`, `style_pages.css`, `script_pages.js`, `README.md`, `requirements.txt` |

---

## 📦 Dependencies

```
flask>=3.0.0
tensorflow>=2.15.0
numpy>=1.24.0
Pillow>=10.0.0
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 🗂️ plant_disease.json Format

The disease information file must be a JSON array ordered by class index (alphabetical by training folder name):

```json
[
  {
    "name": "Apple___Apple_scab",
    "cause": "Caused by the fungus Venturia inaequalis...",
    "cure": "Apply fungicides such as captan or myclobutanil..."
  },
  {
    "name": "Apple___Black_rot",
    "cause": "Caused by the fungus Botryosphaeria obtusa...",
    "cure": "Remove infected fruit and branches. Apply copper-based sprays..."
  }
]
```

> ⚠️ The array order **must exactly match** the class index order used during training. Use the `/debug` endpoint to verify.

---
