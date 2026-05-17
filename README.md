---
title: EcoScan AI Smart Waste Detection
emoji: ♻️
colorFrom: green
colorTo: teal
sdk: docker
pinned: false
app_port: 7860
---

# EcoScan AI - Smart Waste Detection Dashboard

EcoScan AI is a premium, state-of-the-art web application powered by **YOLOv8**, **Flask**, and **OpenCV** designed to classify and detect garbage in real-time. It includes a beautiful white-themed SaaS dashboard, supports multi-media uploads (images/videos), features a pre-loaded test corpus, and integrates a **Local Device Camera Streamer** optimized for mobile browsers and cloud hosting compatibility.

---

## Features

* **Mobile Camera Capture**: HTML5-powered browser video stream allows mobile devices (Safari/Chrome) to stream their rear/front cameras, bypass server hardware limitations, and perform real-time waste scanning.
* **Server Webcam Feed**: Native OpenCV webcam capture for local desktop hosting.
* **Multi-Media Uploader**: Drag-and-drop zone that handles custom image uploads (instant analysis) and video uploads (streams frame-by-frame through the YOLOv8 pipeline).
* **Quick Samples Gallery**: Instant click-to-test gallery loaded with sample images.
* **AI Threshold Controller**: A reactive range slider to dynamically alter YOLOv8's confidence thresholds.
* **Real-Time Analytics**: Live statistics listing all identified waste objects with precise model confidence percentages.
* **Eco-Insight Hub**: Dynamic recycling facts and sorting suggestions that update reactively.

---

## Tech Stack
* **AI Model**: YOLOv8 (Ultralytics) - custom trained for garbage detection
* **Backend**: Flask (Python)
* **Frontend**: HTML5, Vanilla CSS, Vanilla JavaScript
* **Production Server**: Gunicorn (WSGI Web Server)
* **Deployment**: Dockerized to run on Hugging Face Spaces, Render, and Railway

---

## Deployment Instructions

This project is pre-configured and 100% ready for instant deployment across three premier platforms:

### 1. Render
* **Service Type**: Web Service
* **Runtime**: `Python`
* **Build Command**:
  ```bash
  pip install --upgrade pip && pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu && pip install -r requirements.txt
  ```
* **Start Command**: `gunicorn app:app`

### 2. Railway
Railway will automatically detect the `Dockerfile` or `Procfile` in the root of this repository.
* Simply connect your GitHub repository and click **Deploy**.
* Railway will containerize your application and run it on a public domain automatically.

### 3. Hugging Face Spaces
* Create a new **Space** on Hugging Face.
* Choose **Docker** as the SDK (instead of Streamlit or Gradio).
* Select the **Blank** template.
* Push this repository to the Hugging Face space remote repository.
* Hugging Face will read the frontmatter metadata in this `README.md` and build your container on port `7860` automatically!

---

## Local Setup

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <your-repo-url>
   cd garbage_detection
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   python app.py
   ```
4. Access the application in your browser at `http://localhost:5000`.
