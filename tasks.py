from celery import Celery #Narzędzia do obsługi zadań asynchronicznych
import os
import requests
import cv2

#Konfiguracja Celery z użyciem Redis jako brokera i backendu
celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

#Definiowanie kolejek zadań dla poszczególnych funkcji
celery.conf.task_routes = {
    "tasks.detect_people_from_file": {"queue": "image_queue"},
    "tasks.detect_people_from_url": {"queue": "image_queue"}
}

#Dodatkowe ustawienia Celery
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)

#Funkcja do detekcji ludzi na obrazie.
def detect_people(image_path):
    #Wczytanie modelu detekcji ludzi z plików TensorFlow
    net = cv2.dnn.readNetFromTensorflow(
        "models/frozen_inference_graph.pb",
        "models/faster_rcnn_resnet50_coco_2018_01_28.pbtxt"
    )

    image = cv2.imread(image_path)
    height, width, _ = image.shape

    #Przygotowanie obrazu do analizy (blob)
    blob = cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward()

    count = 0
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2] #Pewność detekcji
        class_id = int(detections[0, 0, i, 1])

        if confidence > 0.5 and class_id == 0:  #Filtr: pewność > 0.5 i obiekt to człowiek
            count += 1
            x1 = int(detections[0, 0, i, 3] * width)
            y1 = int(detections[0, 0, i, 4] * height)
            x2 = int(detections[0, 0, i, 5] * width)
            y2 = int(detections[0, 0, i, 6] * height)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    #Zapisanie przetworzonego obrazu z zaznaczonymi osobami
    output_path = f"static/processed_{image_path.split('/')[-1]}"
    cv2.imwrite(output_path, image)
    return count, output_path  #Zwraca liczbę wykrytych osób i ścieżkę do przetworzonego obrazu

#Zadanie Celery: detekcja ludzi z pliku lokalnego
@celery.task
def detect_people_from_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"brak pliku {file_path}")

    image = cv2.imread(file_path)
    if image is None:
        raise ValueError(f"brak pliku {file_path}")

    count, output = detect_people(file_path)
    return {"ludzi": count, "lokalizacja": output}

#Zadanie Celery: detekcja ludzi z obrazu pobranego z URL.
@celery.task
def detect_people_from_url(url):
    response = requests.get(url)
    image_path = f"static/temp_{url.split('/')[-1]}"
    with open(image_path, 'wb') as f:
        f.write(response.content)
    count, output = detect_people(image_path)
    return {"ludzi": count, "lokalizacja": output}
