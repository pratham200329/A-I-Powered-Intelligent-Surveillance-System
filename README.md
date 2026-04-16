# Smart Visitor Detection, Tracking and Behavior Analysis System

Industry-grade surveillance platform combining real-time computer vision and machine learning for visitor recognition, trajectory tracking, behavior learning, and anomaly alerting.

## 1) What this system does

- Real-time person detection with YOLOv8
- Face recognition using dlib embeddings (via face_recognition)
- Multi-object tracking with ByteTrack and persistent IDs
- Behavior classification into normal or suspicious visitors (Random Forest)
- Unsupervised anomaly detection (Isolation Forest)
- Peak hour forecasting for visits (time-series regression)
- Visitor segmentation using K-Means clustering
- Multi-camera ingestion and stream processing
- FastAPI backend and web dashboard
- Alerting by email and SMS (Twilio)
- CSV export and historical analytics

## 2) Architecture

- cv_module: detection, tracking, recognition, feature engineering
- data_pipeline: camera ingest, stream processor, feature store
- ml_models: training and inference for all behavior models
- backend: FastAPI APIs, DB models, analytics and ML services
- frontend: live monitoring dashboard with charts
- utils: config, logging, alerts, exports

## 3) Project structure

- cv_module/
- ml_models/
- backend/
- frontend/
- data_pipeline/
- utils/
- data/
- requirements.txt

## 4) ML model design and why each is used

### Behavior classification (Random Forest)
Input features:
- duration_seconds
- avg_speed
- area_coverage
- repeated_visit_count
- odd_hour_visit

Why this model:
- Strong tabular baseline
- Handles non-linear relationships and feature interactions
- Robust with noisy real-world behavior signals

Output:
- normal
- suspicious

### Anomaly detection (Isolation Forest)
Input features:
- same behavior features as classifier

Why this model:
- Unsupervised and practical for unknown anomaly patterns
- Works well with mixed-scale tabular behavior vectors

Output:
- anomaly_score
- is_anomaly_prediction

### Visit prediction (time-series regression)
Model:
- RandomForestRegressor with lag features and cyclical time encoding

Why this model:
- Captures non-linear seasonality patterns without deep-model overhead
- Works even with limited historical volume

Output:
- forecasted visit counts for upcoming hours

### Clustering (K-Means)
Input features:
- same behavior feature set

Why this model:
- Effective for operational cohorting of visitor behavior profiles
- Enables grouped policies and smarter monitoring

Output groups (example):
- frequent visitors
- rare visitors
- unknown pattern visitors

## 5) Feature engineering details

The pipeline extracts features from each tracked visitor session:

- Duration:
  - exit_time - entry_time
- Movement speed:
  - total center-point travel distance divided by session duration
- Area coverage:
  - normalized bounding region occupied by trajectory over frame area
- Repeated visit count:
  - number of historical visits for the same identity
- Odd-hour indicator:
  - 1 for night/odd hours, 0 otherwise
- Trajectory:
  - list of center points, persisted for heatmap analytics

## 6) Database entities

- visitors:
  - external_id, name, known/unknown, face embedding
- visit_logs:
  - entry/exit, camera id, track id, trajectory, behavior features, ML outputs
- alerts:
  - alert_type, severity, message, visitor/camera linkage, status

## 7) Setup guide

## Step 1: Create environment

Windows PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

Copy environment config:

copy .env.example .env

## Step 2: Optional - generate bootstrap dataset

python data_pipeline/generate_sample_data.py

## Step 3: Train ML models

python train_models.py --dataset data/behavior_dataset.csv

Or train from already captured DB logs:

python train_models.py --from-db

## Step 4: Start backend + dashboard

python run_backend.py

Open:

http://localhost:8000

## Step 5: Enroll known visitors

python seed_known_visitor.py --external-id EMP_001 --name "John" --image path_to_face.jpg

## Step 6: Run standalone real-time pipeline (optional)

python run_realtime.py --source 0 --camera-id cam_local

## 8) API summary

- POST /api/visitors
  - enroll known visitor with image
- GET /api/visitors
  - list known and unknown identities
- GET /api/logs
  - visit logs
- GET /api/alerts
  - anomaly and suspicious alerts
- PATCH /api/alerts/{alert_id}/workflow
  - acknowledge, assign, resolve, reopen, add notes
- GET /api/analytics
  - KPI, hourly, daily, weekly distributions
- GET /api/analytics/heatmap
  - movement heatmap matrix
- GET /api/analytics/forecast
  - predicted future visit counts
- POST /api/ml/retrain
  - retrain all ML models
- POST /api/ml/predict
  - apply latest ML predictions to logs
- GET /api/export/logs
  - CSV export
- GET /api/export/incidents/{alert_id}
  - ZIP evidence package (alert metadata, workflow timeline, related logs)
- POST /api/cameras/start
- POST /api/cameras/stop
- GET /api/cameras/status/{camera_id}
- GET /api/cameras/status
- GET /api/live/{camera_id}

## 9) Notes for production

- Use PostgreSQL instead of SQLite for concurrency
- Place YOLO and tracking workers behind message queue for scale
- Use GPU inference and model quantization for higher FPS
- Add role-based auth and audit logs for compliance
- Add per-zone rules for restricted areas and geofencing alerts

## 10) Evaluation artifacts

After training, metrics are saved at:

- data/ml_artifacts/metrics.json

Model artifacts are stored at:

- data/ml_artifacts/*.joblib
