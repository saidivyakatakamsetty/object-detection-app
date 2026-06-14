# 🎯 VisionAI — Real-Time Object Detection App

A production-ready object detection application powered by YOLOv8 and Gradio. Detects 80+ object classes in images, videos, and live webcam feeds in real time.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange?style=flat-square)
![Gradio](https://img.shields.io/badge/Gradio-UI-green?style=flat-square)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red?style=flat-square)

---

## ✨ Features

- 🖼️ **Image Detection** — upload any photo and detect all objects instantly
- 🎥 **Video Processing** — run detection on full video files with annotated output
- 📷 **Live Webcam** — real-time detection stream in the browser
- ⚡ **True Real-Time Mode** — OpenCV-powered live window at full speed
- 🤖 **4 Model Sizes** — switch between Nano, Small, Medium, and Large YOLOv8
- 🎛️ **Confidence Control** — adjustable detection threshold slider
- 🌐 **Clean Web UI** — dark futuristic interface with Space Grotesk font

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Object Detection | YOLOv8 (Ultralytics) |
| Deep Learning | PyTorch |
| Web Interface | Gradio |
| Computer Vision | OpenCV |
| Image Processing | Pillow |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/saidivyakatakamsetty/object-detection-app.git
cd object-detection-app
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install torch torchvision ultralytics gradio opencv-python Pillow
```

### 4. Run the web app
```bash
python app.py
```
Open your browser at **http://127.0.0.1:7860**

### 5. Run true real-time webcam detection
```bash
python webcam_live.py
```
Press **Q** to quit the webcam window.

---

## 📁 Project Structure

object-detection-app/

├── app.py            # Gradio web interface

├── detector.py       # YOLOv8 detection logic

├── webcam_live.py    # Real-time OpenCV webcam window

└── README.md

---

## 🎯 Detectable Objects

YOLOv8 can detect 80 object classes including:
people, cars, trucks, buses, bicycles, motorcycles, animals, furniture, electronics, food, sports equipment, and much more.

---

## 📊 Model Options

| Model | Speed | Accuracy | Best For |
|-------|-------|----------|----------|
| Nano | ⚡⚡⚡⚡ | ⭐⭐ | Real-time, low-power |
| Small | ⚡⚡⚡ | ⭐⭐⭐ | Balanced |
| Medium | ⚡⚡ | ⭐⭐⭐⭐ | Higher accuracy |
| Large | ⚡ | ⭐⭐⭐⭐⭐ | Maximum accuracy |

---

## 🌍 Applications

This project demonstrates skills applicable across many industries:
- **Autonomous Vehicles** — real-time road object detection
- **Manufacturing** — defect and anomaly detection
- **Retail** — product and inventory recognition
- **Security** — surveillance and threat detection
- **Healthcare** — medical imaging analysis
- **Agriculture** — crop and pest detection
