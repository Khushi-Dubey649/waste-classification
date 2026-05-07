# ♻️ Automated Waste Classification System using Deep Learning

> Classifies waste into 6 categories in real-time using EfficientNetB0 with Transfer Learning — achieving **97.15% accuracy**, surpassing the existing research benchmark of 96.78%.

🚀 **[Live Demo on Hugging Face Spaces](https://huggingface.co/spaces/khushi-dubey-03/waste-classifier)**

---

## 📌 Overview

This project is an AI-powered web application that automatically classifies waste images into one of 6 categories to assist with proper waste disposal and recycling. The model is trained on 8,810 images using EfficientNetB0 with a 2-phase Transfer Learning strategy.

---

## 🗂️ Waste Categories

| Category | Examples |
|----------|----------|
| 🟢 Cardboard | Boxes, packaging |
| 🟢 Glass | Bottles, jars |
| 🟢 Metal | Cans, foil |
| 🟢 Paper | Newspapers, office paper |
| 🟢 Plastic | Bags, bottles, containers |
| 🔴 Trash | General non-recyclable waste |

---

## 🧠 Model Architecture

- **Base Model:** EfficientNetB0 (pretrained on ImageNet)
- **Strategy:** 2-Phase Transfer Learning
  - Phase 1: Freeze base layers, train classifier head
  - Phase 2: Unfreeze top layers, fine-tune end-to-end
- **Dataset:** Combined TrashNet + additional garbage dataset (8,810 images)
- **Final Accuracy: 97.15%** (Research paper baseline: 96.78%)

### Training Progress

| Phase | Accuracy |
|-------|----------|
| Baseline (random) | ~28% |
| Phase 1 (frozen base) | ~91% |
| Phase 2 (fine-tuned) | **97.15%** |

---

## ✨ App Features

1. **📸 Image Upload Classification** — Upload any waste image for instant classification
2. **🎥 Real-time Webcam Classification** — Live waste detection via webcam
3. **🌱 CO2 Impact Calculator** — Shows estimated CO2 savings from correct recycling
4. **📍 Nearest Bin Locator** — Suggests nearest disposal/recycling point
5. **🎨 Color-coded Feedback System** — Green / Yellow / Red results with Recycling Impact Score

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python |
| Deep Learning | TensorFlow, Keras |
| Model | EfficientNetB0, Transfer Learning |
| Web Interface | Gradio |
| Deployment | Hugging Face Spaces |
| Data Processing | NumPy, PIL |
| Development | Google Colab, Google Drive |

---

## 📁 Repository Structure

```
waste-classification/
│
├── waste_classification.ipynb   # Training notebook (Google Colab)
├── app.py                       # Gradio web app
├── requirements.txt             # Dependencies
└── README.md
```

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/waste-classification.git
cd waste-classification

# Install dependencies
pip install -r requirements.txt

# Launch the app
python app.py
```

---

## 📦 Requirements

```
tensorflow
keras
gradio
numpy
pillow
```

---

## 📊 Results

| Metric | Value |
|--------|-------|
| Test Accuracy | **97.15%** |
| Research Baseline | 96.78% |
| Dataset Size | 8,810 images |
| Classes | 6 |
| Model | EfficientNetB0 |

