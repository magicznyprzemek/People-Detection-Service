from fastapi import FastAPI, UploadFile, Form, File
import os
from celery.result import AsyncResult
from tasks import detect_people_from_file, detect_people_from_url
app = FastAPI()

#Endpoint do wykrywania osób z przesłanego pliku
@app.post("/detect/file")
async def detect_from_file(file: UploadFile = File(...)):
    save_dir = os.path.abspath("static")
    os.makedirs(save_dir, exist_ok=True)
    image_path = os.path.join(save_dir, f"temp_{file.filename}")

    #Zapisuje przesłany plik w lokalnym systemie plików
    with open(image_path, 'wb+') as f:
        f.write(file.file.read())
    print(f"zapisano -> {image_path}")

    #Uruchamia zadanie Celery do wykrywania osób na obrazie
    task = detect_people_from_file.delay(image_path)
    return {"task id": task.id}

#Endpoint do wykrywania osób z obrazu pobranego z URL
@app.post("/detect/url")
async def detect_from_url(url: str = Form(...)):
    task = detect_people_from_url.delay(url) #Uruchamia zadanie Celery do detekcji osób na podstawie obrazu z URL
    return {"task id": task.id}

#Endpoint do sprawdzania statusu zadania
@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    return {
        "task id": task_id,
        "status": task_result.status,
        "wynik": task_result.result,
    }

