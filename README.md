# 🧠 AI-Powered Intelligent Surveillance System

## 🚀 Overview

The AI-Powered Intelligent Surveillance System is a full-stack, production-grade application designed to transform traditional CCTV systems into intelligent, automated, and proactive monitoring solutions. It leverages advanced computer vision, machine learning, and modern web technologies to detect, track, analyze, and predict human behavior in real time.

---

## ✨ Key Features

### 🎥 Computer Vision Capabilities

* Real-time person detection using **YOLOv8**
* Multi-object tracking using **ByteTrack**
* Frame-by-frame analysis with OpenCV
* Optional face recognition support

### 🤖 Machine Learning Intelligence

* Behavior Classification (Normal, Suspicious, Loitering, etc.)
* Anomaly Detection (Isolation Forest)
* Visitor Clustering (K-Means)
* Visit Prediction (LightGBM/XGBoost)

### 📊 Dashboard & Analytics

* Real-time camera feed monitoring
* Heatmaps for visitor activity
* Behavior distribution charts
* Visit trend forecasting
* Incident replay system

### 🚨 Alert System

* Automated anomaly alerts
* Email notifications (SMTP)
* SMS alerts via Twilio
* Alert workflow (Open → Acknowledged → Resolved)

### 🧩 Additional Features

* Zone-based rule enforcement
* AI Copilot for natural language queries
* Data export (CSV/JSON/ZIP evidence)
* Model explainability (feature importance)

---

## 🏗️ System Architecture

The system follows a **4-layer modular architecture**:

1. **Computer Vision Layer** – Detection & Tracking
2. **Data Pipeline Layer** – Feature Engineering & Processing
3. **Machine Learning Layer** – Predictions & Insights
4. **Application Layer** – Backend API + Frontend Dashboard

---

## 🧰 Tech Stack

### Backend

* FastAPI (REST API)
* Python 3.10+
* SQLAlchemy (ORM)
* SQLite / PostgreSQL

### Frontend

* React.js (SPA)
* Chart libraries & visualization tools

### AI/ML

* YOLOv8 (Ultralytics)
* ByteTrack
* Scikit-learn
* LightGBM / XGBoost

### DevOps

* Docker & Docker Compose
* Environment-based configuration

---

## 🗄️ Database Schema

Main Tables:

* visitors
* visit_logs
* alerts
* alert_workflows
* zone_rules

All relationships are managed using foreign keys and ORM.

---

## ⚙️ Installation Guide

### Prerequisites

* Python 3.10+
* Node.js 18+
* Docker (optional)

### 🔧 Backend Setup

```bash
git clone https://github.com/your-username/ai-surveillance-system.git
cd ai-surveillance-system

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows

pip install -r requirements.txt
cp .env.example .env

python -m backend.db.init_db
python -m ml_models.train_all

uvicorn backend.main:app --reload
```

Backend runs at: [http://localhost:8000](http://localhost:8000)

---

### 💻 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: [http://localhost:5173](http://localhost:5173)

---

## 🐳 Docker Setup

```bash
docker compose build
docker compose up -d
```

Services:

* API → [http://localhost:8000](http://localhost:8000)
* Dashboard → [http://localhost:80](http://localhost:80)

---

## 🔐 Security Features

* Secure API design
* Environment-based secrets
* Alert workflows & audit tracking
* Prepared for RBAC integration

---

## 📈 Performance

* 15 FPS (CPU) / 30+ FPS (GPU)
* Behavior Classification Accuracy: **99.49%**
* Anomaly Detection ROC-AUC: **0.83**

---

## 🚀 Future Enhancements

* GPU-based inference scaling
* Role-Based Access Control (RBAC)
* Cloud deployment (AWS/GCP/Azure)
* Advanced AI Copilot with LLMs
* Multi-camera tracking (Re-ID)

---

## 👨‍💻 Author

**Riya Raina**
MCA – Chandigarh University

---

## 📄 License

This project is for academic and educational purposes.

---

⭐ If you found this project useful, give it a star!
