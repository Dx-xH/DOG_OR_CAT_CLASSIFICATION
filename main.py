# diff --git a/c:\PBEL\DOGCATCL\app/main.py b/c:\PBEL\DOGCATCL\app/main.py
# new file mode 100644
# --- /dev/null
# +++ b/c:\PBEL\DOGCATCL\app/main.py
# @@ -0,0 +1,50 @@
import io

import numpy as np
import requests
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image

app = FastAPI()
templates = Jinja2Templates(directory="templates")

TF_SERVING_URL = "http://tfserving:8501/v1/models/cat_dog_model_TF:predict"
IMG_SIZE = 150


def preprocess_image(image: Image.Image):
    image = image.resize((IMG_SIZE, IMG_SIZE))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image.tolist()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": None, "error_message": None},
    )


@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")
    processed_image = preprocess_image(image)

    try:
        response = requests.post(
            TF_SERVING_URL,
            json={"instances": processed_image},
            timeout=30,
        )
        response.raise_for_status()
        prediction = float(response.json()["predictions"][0][0])
    except requests.RequestException as exc:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "error_message": f"Prediction failed: {exc}",
            },
            status_code=502,
        )

    is_dog = prediction > 0.5
    result = {
        "label": "Dog" if is_dog else "Cat",
        "icon": "DOG" if is_dog else "CAT",
        "prediction_score": prediction,
        "confidence": prediction if is_dog else 1 - prediction,
    }

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": result, "error_message": None},
    )
