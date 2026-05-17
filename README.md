---
title: EcoScan AI Smart Waste Detection
emoji: ♻️
colorFrom: green
colorTo: teal
sdk: docker
pinned: false
app_port: 7860
---

<div align="center">
  <h1>♻️ EcoScan AI</h1>
  <h3>Smart Waste Detection & Real-Time Classification Dashboard</h3>
  <p><em>Empowering communities with computer vision to automate, track, and optimize waste recycling.</em></p>

  <p>
    <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"></a>
    <a href="https://flask.palletsprojects.com"><img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"></a>
    <a href="https://github.com/ultralytics/ultralytics"><img src="https://img.shields.io/badge/YOLOv8-Ultralytics-FF2F2F?style=for-the-badge" alt="YOLOv8"></a>
    <a href="https://opencv.org"><img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV"></a>
    <a href="https://docker.com"><img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"></a>
  </p>
</div>

---

## 📖 Table of Contents
- [Project Overview](#-project-overview)
- [⚡ Model Performance & Metrics](#-model-performance--metrics)
- [🌟 Key Features](#-key-features)
- [🛠️ Tech Stack](#-tech-stack)
- [💻 Local Setup & Execution](#-local-setup--execution)
- [🚀 Production & Cloud Deployment](#-production--cloud-deployment)
- [📂 Project Directory Structure](#-project-directory-structure)
- [🤝 Contributing & License](#-contributing--license)

---

## 📖 Project Overview

**EcoScan AI** is a premium, high-performance web dashboard powered by custom-trained **YOLOv8** object detection models, a robust **Flask** backend, and **OpenCV** processing pipelines. 

Designed with a modern, responsive, white-themed SaaS dashboard, it resolves real-world ecological sorting problems by classifying and detecting everyday garbage categories in real-time. The application is highly optimized, featuring dual modes for desktop (native OpenCV stream) and mobile environments (HTML5-powered streamer), bypassing traditional cloud hardware limitations.

---

## ⚡ Model Performance & Metrics

The core intelligence of EcoScan AI is powered by a custom-trained **YOLOv8** object detector tailored specifically for garbage classification. Under strict validation benchmarks, the model displays exceptional capabilities:

| Metric | Value | Interpretation |
| :--- | :--- | :--- |
| **mAP50** | **76%** | High overall detection accuracy across all designated waste categories. |
| **Precision** | **87%** | Extreme reliability in classifications, ensuring minimal false-positive alarms. |
| **Recall** | **66%** | High sensitivity in capturing target waste objects under varying lighting and cluttered environments. |

### 📈 Metrics Breakdown & Insights
* **Precision-First Architecture**: With an **87% Precision** score, the system is designed to minimize sorting errors, ensuring that recyclables are not incorrectly classified as landfill materials, which is crucial for real-world sorting plants.
* **Generalization**: The **76% mAP50** demonstrates robust performance in detecting smaller objects, complex trash overlaps, and deformed plastic/paper waste in diverse settings.

---

## 🌟 Key Features

* 📱 **Mobile-Optimized Camera Streamer**: Runs an HTML5 client-side video feed to capture camera frames on mobile devices (Safari/Chrome), streaming them directly to the backend API. This completely bypasses local USB webcam constraints and enables cloud hosting on servers without physical camera access.
* 🖥️ **Native Desktop Webcam Feed**: Integrates OpenCV `VideoCapture` streams for direct, low-latency analysis when hosted locally on hardware with an active webcam.
* 📁 **Smart Multi-Media Uploader**: Features an interactive drag-and-drop zone that performs instant inference on uploaded images and processes pre-recorded video files frame-by-frame.
* 🖼️ **Quick-Test Samples Gallery**: A curated carousel of pre-loaded trash samples to showcase YOLOv8 inference speed and bounding box generation within seconds.
* 🎚️ **Interactive Confidence Controller**: A responsive front-end slider that dynamically modifies the YOLOv8 model's confidence threshold (`conf_threshold`) in real-time, allowing users to fine-tune sensitivity.
* 📊 **Live Statistical Insights**: Computes real-time data detailing all identified objects, coordinate bounding boxes, and precision statistics, accompanied by dynamic recycling instructions.

---

## 🛠️ Tech Stack

- **Computer Vision & Inference**: [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) (Neural Networks), OpenCV (Image Manipulation & Video I/O)
- **Backend Infrastructure**: [Flask](https://flask.palletsprojects.com/) (Python-based micro-framework)
- **Frontend Layer**: HTML5 (Semantic Structure), Vanilla CSS (Premium, modern white SaaS aesthetic), JavaScript (Asynchronous client-side logic, API streaming)
- **Containerization & WSGI**: Docker (Multi-stage builds), Gunicorn (Production-ready WSGI web server)

---

## 💻 Local Setup & Execution

Follow these step-by-step instructions to clone, configure, and execute EcoScan AI on your local computer.

### 📋 Prerequisites
Ensure you have the following installed on your system:
- **Python 3.8 to 3.11** (Python 3.12+ is supported, but 3.8-3.11 is recommended for pre-compiled PyTorch wheels)
- **Git**

---

### 📥 Step-by-Step Installation

#### 1. Clone the Repository
Open your terminal (PowerShell, CMD, or Bash) and run:
```bash
git clone <your-repository-url>
cd garbage_detection
```

#### 2. Initialize a Virtual Environment (Highly Recommended)
Creating an isolated virtual environment prevents library version conflicts:

* **On Windows (PowerShell/CMD):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
* **On macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

#### 3. Install Required Dependencies
First, upgrade `pip` and then install the required Python packages:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
> 💡 *Note: If you have an NVIDIA GPU and want to use CUDA acceleration, make sure to install PyTorch with CUDA support beforehand by following instructions on the [Official PyTorch Website](https://pytorch.org/).*

#### 4. Model Configuration
Ensure your custom-trained YOLOv8 weights file is placed in the root directory:
- Name: `best.pt` (Must match the configuration inside `app.py`)
- *Already pre-loaded in this repository!*

#### 5. Launch the Application
Run the Flask server:
```bash
python app.py
```

#### 6. Access the Dashboard
Once the server initializes, open your favorite web browser and navigate to:
```
http://localhost:5000
```

---

## 🚀 Production & Cloud Deployment

EcoScan AI is 100% pre-configured for seamless containerized and server-based deployments:

### 1. Render Deployment (Python Service)
- **Service Type**: `Web Service`
- **Runtime**: `Python`
- **Build Command**:
  ```bash
  pip install --upgrade pip && pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu && pip install -r requirements.txt
  ```
- **Start Command**: `gunicorn app:app`

### 2. Railway Deployment (Docker/Procfile)
Railway automatically detects the root `Dockerfile` or `Procfile`.
- Connect your GitHub repository to Railway.
- Create a new project -> Deploy from GitHub repo.
- Railway will handle the Docker build, bind to the correct port, and expose a secure URL.

### 3. Hugging Face Spaces (Dockerized)
- Create a new Hugging Face **Space**.
- Choose **Docker** as the SDK.
- Select the **Blank** template.
- Push the repository to the Space's Git remote. Hugging Face will automatically parse the YAML metadata block at the top of the `README.md` and deploy the container on port `7860`.

---

## 📂 Project Directory Structure

```plaintext
garbage_detection/
├── app.py                   # Main Flask application with API and streaming logic
├── best.pt                  # Custom trained YOLOv8 model weights (76% mAP50)
├── yolov8n.pt               # Pre-trained base YOLOv8 model
├── Dockerfile               # Production Docker container configuration
├── Procfile                 # Process file for Heroku/Railway deployment
├── requirements.txt         # Project python dependencies
├── static/                  # Static assets (stylesheets, icons, samples)
│   ├── css/
│   ├── js/
│   └── test_images/         # Quick-test sample images
├── templates/               # UI HTML files
│   └── index.html           # Main dashboard template
└── README.md                # Interactive documentation (this file)
```

---

## 🤝 Contributing & License

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

<div align="center">
  <p>Developed with ❤️ by the EcoScan AI Team.</p>
</div>
