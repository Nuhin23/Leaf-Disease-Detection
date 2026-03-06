"""
LeafAI - Plant Disease Detection App

FIXES FOR "ALWAYS SAME PREDICTION" BUG:
─────────────────────────────────────────────────────────────────
Root cause is almost always one of three things:

  1. NORMALIZATION MISMATCH
     If your model was trained with a Keras ImageDataGenerator that uses
     preprocessing_function=preprocess_input (e.g. MobileNet, EfficientNet,
     ResNet), those models expect pixels in [-1, 1] or a specific channel
     shift — NOT simple /255 normalization.
     ➜ Fix: auto-detect backbone and apply the correct preprocess_input.

  2. INPUT SIZE MISMATCH
     If the model was trained on 224×224 but we pass 160×160 (or vice versa),
     the spatial features don't align and the model always picks the "safe"
     majority class.
     ➜ Fix: read the actual input shape from the model itself.

  3. RGBA / PALETTE IMAGE
     PNG files can have 4 channels (RGBA) or be palette mode ('P').
     Converting these to array without forcing RGB gives wrong channel count.
     ➜ Fix: force color_mode='rgb' so we always get exactly 3 channels.

  4. JSON INDEX MISMATCH
     If plant_disease.json is not in the exact same class order as used during
     training (alphabetical by folder name for ImageDataGenerator), class
     indices are wrong even if the prediction itself is correct.
     ➜ Fix: added /debug endpoint to print raw probabilities so you can verify.
─────────────────────────────────────────────────────────────────
"""

from flask import Flask, render_template, request, redirect, send_from_directory, url_for, jsonify
import numpy as np
import json
import uuid
import tensorflow as tf
import os
import base64
import re

app = Flask(__name__)

# ==============================
# Configuration
# ==============================
UPLOAD_FOLDER = "uploadimages"
MODEL_PATH    = "models/plant_disease_model.keras"
JSON_PATH     = "plant_disease.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==============================
# Load Model & Disease Info
# ==============================
model = tf.keras.models.load_model(MODEL_PATH)

# ── Read the model's expected input size directly from its config ──────────
# This prevents size mismatches if training used a different size than 160×160
_input_shape = model.input_shape          # e.g. (None, 224, 224, 3)
IMG_HEIGHT   = _input_shape[1]            # e.g. 224
IMG_WIDTH    = _input_shape[2]            # e.g. 224
print(f"[LeafAI] Model expects input: {IMG_HEIGHT}x{IMG_WIDTH} px")

# ── Detect which base model / preprocessing was used ──────────────────────
# We inspect the model's layer names to auto-detect the backbone.
# If you built a custom CNN with /255 normalization, set PREPROCESS_MODE = 'divide255'
layer_names = [l.name.lower() for l in model.layers]

if   any('efficientnet' in n for n in layer_names):
    PREPROCESS_MODE = 'efficientnet'
elif any('mobilenet'    in n for n in layer_names):
    PREPROCESS_MODE = 'mobilenet'
elif any('resnet'       in n for n in layer_names) or any('vgg' in n for n in layer_names):
    PREPROCESS_MODE = 'caffe'         # ResNet/VGG use channel-mean subtraction
elif any('inception'    in n for n in layer_names):
    PREPROCESS_MODE = 'tf'            # Inception uses [-1, 1] scaling
else:
    PREPROCESS_MODE = 'divide255'     # Custom CNN with plain /255

print(f"[LeafAI] Preprocessing mode auto-detected: {PREPROCESS_MODE}")
print("[LeafAI] If predictions still seem wrong, override PREPROCESS_MODE manually above.")

# Load disease info JSON — must be a list ordered by class index from training
with open(JSON_PATH, 'r') as f:
    plant_disease = json.load(f)

print(f"[LeafAI] Loaded {len(plant_disease)} disease classes from JSON.")


# ==============================
# Serve Uploaded Images
# ==============================
@app.route('/uploadimages/<path:filename>')
def uploaded_images(filename):
    """Serve saved images from the upload folder to the template."""
    return send_from_directory(UPLOAD_FOLDER, filename)


# ==============================
# Home Page
# ==============================
@app.route('/')
def home():
    return render_template('home.html')


# ==============================
# Coverage Page
# ==============================
@app.route('/coverage')
def coverage():
    """Shows all plants and disease classes the model can diagnose."""
    return render_template('coverage.html')


# ==============================
# Predict Page  (GET + POST)
# ==============================
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """
    GET  -> show empty prediction form
    POST -> accept either:
              - a file upload  (multipart form field: 'image')
              - a base64 image from the camera (form field: 'captured_image')
           then run the model and render results
    """
    if request.method == 'POST':

        unique_name = f"{uuid.uuid4().hex}.jpg"
        save_path   = os.path.join(UPLOAD_FOLDER, unique_name)

        # ── Path A: Camera capture (base64 data-URL from JS) ─────────────────
        captured_b64 = request.form.get('captured_image', '')
        if captured_b64:
            b64_data  = re.sub(r'^data:image/\w+;base64,', '', captured_b64)
            img_bytes = base64.b64decode(b64_data)
            with open(save_path, 'wb') as img_file:
                img_file.write(img_bytes)

        # ── Path B: File upload ───────────────────────────────────────────────
        else:
            if 'image' not in request.files:
                return redirect('/predict')
            image = request.files['image']
            if image.filename == "":
                return redirect('/predict')
            image.save(save_path)

        # ── Run model ─────────────────────────────────────────────────────────
        prediction, confidence = model_predict(save_path)

        return render_template(
            'predict.html',
            imagepath  = url_for('uploaded_images', filename=unique_name),
            prediction = prediction,
            confidence = confidence
        )

    return render_template('predict.html')


# ==============================
# DEBUG Endpoint
# ==============================
@app.route('/debug', methods=['GET', 'POST'])
def debug():
    """
    ─────────────────────────────────────────────────────────────
    DIAGNOSTIC TOOL — visit http://127.0.0.1:5000/debug

    POST an image to see:
      - Raw probability for EVERY class
      - Top-5 predicted classes with their JSON names
      - Active preprocessing mode
      - Model input shape

    This instantly tells you if:
      - One class always gets 99%+ (normalization/size bug)
      - All probabilities are flat/similar (wrong preprocessing)
      - Top class index does not match the name in JSON (index order bug)
    ─────────────────────────────────────────────────────────────
    """
    if request.method == 'POST':
        image = request.files.get('image')
        if not image:
            return jsonify({"error": "No image uploaded"})

        tmp_path = os.path.join(UPLOAD_FOLDER, f"debug_{uuid.uuid4().hex}.jpg")
        image.save(tmp_path)

        arr    = extract_features(tmp_path)
        output = model.predict(arr)[0]   # shape: (num_classes,)

        # Build top-5 results
        top5_indices = np.argsort(output)[::-1][:5]
        top5 = []
        for rank, i in enumerate(top5_indices):
            name = plant_disease[i]['name'] if i < len(plant_disease) else f"CLASS_{i}"
            top5.append({
                "rank":        rank + 1,
                "index":       int(i),
                "name":        name,
                "probability": round(float(output[i]) * 100, 4)
            })

        os.remove(tmp_path)

        return jsonify({
            "model_input_size":  f"{IMG_HEIGHT}x{IMG_WIDTH}",
            "preprocess_mode":   PREPROCESS_MODE,
            "num_classes_model": int(len(output)),
            "num_classes_json":  len(plant_disease),
            "top_5_predictions": top5,
            "all_probabilities": [round(float(p) * 100, 4) for p in output],
        })

    # GET -> simple HTML upload form
    return """
    <h2>LeafAI Debug Tool</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/*" required><br><br>
        <button type="submit">Run Debug Prediction</button>
    </form>
    <p style="color:gray;font-size:13px">
        Results are JSON showing raw probabilities for all classes.<br>
        Check: is one class always 99%+? That means preprocessing mismatch.<br>
        Check: does the top class name match what you expect? That confirms JSON order.
    </p>
    """


# ==============================
# Image Preprocessing
# ==============================
def extract_features(image_path):
    """
    Load and preprocess one image to exactly match training conditions.

    Key fixes vs. original code:
      1. target_size reads from model.input_shape (no hardcoded 160x160)
      2. color_mode='rgb' forces 3-channel output (fixes PNG/RGBA bugs)
      3. Preprocessing function matches the backbone used in training
    """
    # Load and resize to the model's required size, force 3-channel RGB
    image = tf.keras.utils.load_img(
        image_path,
        target_size = (IMG_HEIGHT, IMG_WIDTH),
        color_mode  = 'rgb'               # prevents RGBA / grayscale bugs
    )
    arr = tf.keras.utils.img_to_array(image)   # shape: (H, W, 3), values 0-255

    # ── Apply the correct preprocessing for the backbone ──────────────────
    if PREPROCESS_MODE == 'efficientnet':
        # EfficientNet: has built-in rescaling — do NOT divide by 255
        arr = tf.keras.applications.efficientnet.preprocess_input(arr)

    elif PREPROCESS_MODE == 'mobilenet':
        # MobileNetV2/V3: scales to [-1, 1]
        arr = tf.keras.applications.mobilenet_v2.preprocess_input(arr)

    elif PREPROCESS_MODE == 'caffe':
        # ResNet50 / VGG: subtracts ImageNet channel means
        arr = tf.keras.applications.resnet.preprocess_input(arr)

    elif PREPROCESS_MODE == 'tf':
        # Inception / Xception: scales to [-1, 1]
        arr = tf.keras.applications.inception_v3.preprocess_input(arr)

    else:
        # Custom CNN trained with simple /255 normalization
        arr = arr / 255.0

    # Add batch dimension: (H, W, 3) -> (1, H, W, 3)
    arr = np.expand_dims(arr, axis=0)
    return arr


# ==============================
# Model Prediction
# ==============================
def model_predict(image_path):
    """
    Run the model and return disease info + confidence.
    Includes a warning if JSON class count doesn't match model output.
    """
    arr    = extract_features(image_path)
    output = model.predict(arr)               # shape: (1, num_classes)

    # ── Sanity check: model output size vs JSON entries ───────────────────
    num_model_classes = output.shape[1]
    if num_model_classes != len(plant_disease):
        print(
            f"[LeafAI] WARNING: Model has {num_model_classes} output classes "
            f"but plant_disease.json has {len(plant_disease)} entries. "
            f"Class index lookup will be wrong — fix your JSON order or count."
        )

    pred_index = int(np.argmax(output))
    confidence = float(np.max(output)) * 100

    # Guard: index out of range
    if pred_index >= len(plant_disease):
        return {
            "disease_name": f"Unknown (class {pred_index})",
            "description":  "Class index not found in JSON. Check class count.",
            "treatment":    "N/A",
        }, round(confidence, 2)

    disease_info   = plant_disease[pred_index]
    formatted_name = (
        disease_info['name']
        .replace("___", " — ")
        .replace("_", " ")
    )

    prediction_data = {
        "disease_name": formatted_name,
        "description":  disease_info.get("cause", "No description available."),
        "treatment":    disease_info.get("cure",  "No treatment info available."),
    }

    return prediction_data, round(confidence, 2)


# ==============================
# Run
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
