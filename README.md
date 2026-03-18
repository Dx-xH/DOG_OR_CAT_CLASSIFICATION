# DOG_OR_CAT_CLASSIFICATION
# 🐶🐱 Cat vs Dog Classifier

A full-stack image classification web app that predicts whether a photo contains a **cat** or a **dog** — built with FastAPI, TensorFlow Serving, and Docker. Upload any pet photo and get an instant prediction with a confidence score.

---

## ✨ Features

- 📸 Upload any image (JPG, PNG, or any Pillow-supported format)
- 🤖 Real-time inference via TensorFlow Serving REST API
- 📊 Confidence score with a visual progress bar
- ⚠️ Graceful error handling — friendly messages shown in UI on failure
- 🎨 Clean, responsive UI with no JavaScript frameworks needed
- 🐳 Fully containerized — one command to run everything

---

## 🧠 How It Works

```
User uploads image
       ↓
FastAPI backend receives file
       ↓
Image resized to 150×150 and normalized (÷255)
       ↓
Sent to TF Serving REST API as JSON payload
       ↓
Model returns a score between 0.0 and 1.0
       ↓
score > 0.5 → 🐶 Dog
score ≤ 0.5 → 🐱 Cat
       ↓
Result + confidence shown in the UI
```

---

## 🗂️ Project Structure

```
DOG_OR_CAT_CLASSIFICATION/
├── docker-compose.yml          # Spins up FastAPI + TF Serving together
├── Dockerfile                  # FastAPI app container definition
├── main.py                     # FastAPI routes, preprocessing, prediction logic
├── requirements.txt            # Python dependencies
├── index.html                  # Jinja2 frontend template (upload form + results)
├── saved_model.pb              # Trained TensorFlow model (graph + weights)
├── fingerprint.pb              # TF model fingerprint metadata
└── smoke-test.jpg              # Sample image for quick testing
```

> The `app/` and `model/` folders need to be set up manually before running — see [Setup](#️-setup--running) below.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| ML Model Serving | TensorFlow Serving (REST API) |
| Backend | FastAPI + Uvicorn |
| Templating | Jinja2 |
| Image Processing | Pillow + NumPy |
| Containerization | Docker + Docker Compose |
| Frontend | Plain HTML + CSS (no JS framework) |

---

## ⚙️ Setup & Running

### Prerequisites

- [Docker](https://www.docker.com/get-started) + [Docker Compose](https://docs.docker.com/compose/) installed and running

### 1. Clone the repository

```bash
git clone https://github.com/Dx-xH/DOG_OR_CAT_CLASSIFICATION.git
cd DOG_OR_CAT_CLASSIFICATION
```

### 2. Set up the model directory

TF Serving requires a **versioned folder** structure:

```bash
mkdir -p model/cat_dog_model_TF/1
cp saved_model.pb model/cat_dog_model_TF/1/
cp fingerprint.pb model/cat_dog_model_TF/1/
```

Expected result:

```
model/
└── cat_dog_model_TF/
    └── 1/
        ├── saved_model.pb
        └── fingerprint.pb
```

### 3. Set up the app directory

The `docker-compose.yml` builds the FastAPI container from an `app/` folder. The template must be inside a `templates/` subfolder:

```bash
mkdir -p app/templates
cp Dockerfile main.py requirements.txt app/
cp index.html app/templates/
```

### 4. Start everything

```bash
docker compose up --build
```

This starts two containers:

| Container | Port | Role |
|---|---|---|
| `tfserving` | `8501` | Serves the TF model via REST |
| `fastapi_app` | `8000` | Serves the web app |

### 5. Open the app

Go to [http://localhost:8000](http://localhost:8000), upload a photo, and see the prediction!

---

## 🔌 API Reference

### `GET /`
Returns the HTML upload page.

### `POST /predict`

Accepts a multipart image upload and returns an HTML page with the prediction result rendered inline.

**Request:**
```
Content-Type: multipart/form-data
Body: file=<image file>
```

**On success**, the page shows:
- Predicted label (`Cat` or `Dog`)
- Confidence percentage
- Raw model score (0.0 – 1.0)
- Visual confidence meter

**On failure** (e.g. TF Serving unreachable), the page shows a friendly error message with HTTP 502.

---

## 🧪 Quick Test (curl)

```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@smoke-test.jpg"
```

---

## 🐛 Troubleshooting

| Problem | Fix |
|---|---|
| TF Serving can't find the model | Confirm `saved_model.pb` is inside `model/cat_dog_model_TF/1/` |
| Port 8000 or 8501 already in use | Edit the port mappings in `docker-compose.yml` |
| `TemplateNotFound` error | Make sure `index.html` is at `app/templates/index.html` |
| "Prediction failed" shown in UI | TF Serving may still be starting — wait a few seconds and retry |
| View live logs | `docker compose logs -f` |
| Rebuild after code changes | `docker compose up --build` |

---

## 📄 License

This project is open source. Feel free to fork and build on it.
