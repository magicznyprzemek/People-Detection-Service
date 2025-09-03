# Person Detection API 
An AI-powered system for detecting people in images, built with Python, FastAPI, Celery, RabbitMQ, and Redis.
This project provides asynchronous image processing with scalable task queues, making it ideal for video surveillance, smart security systems, and real-time monitoring solutions.

## Key Features
- Asynchronous image processing using Celery + RabbitMQ
- People detection powered by TensorFlow
- REST API for easy integration (FastAPI + Swagger UI)
- Real-time monitoring of workers and queue status
- Horizontal scalability – run multiple parallel workers

![screenshot1](pic.jpg)

###  Installation
Clone the repository:
git clone https://github.com/your-username/person-detection-api.git
cd person-detection-api
Download the detection model:
Get the frozen_inference_graph.pb file from here
Place it in the /models/ directory:
/models/frozen_inference_graph.pb
Install dependencies:
pip install -r requirements.txt
### Running the Project
Start Redis server:
redis-server
Run the API (FastAPI):
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
Start Celery workers:
celery -A tasks worker --loglevel=info --concurrency=2 -Q image_queue
concurrency=2 → number of parallel workers
### Testing & Monitoring
1. Swagger UI for API testing:
http://127.0.0.1:8000/docs
2. Check active Celery workers:
celery -A tasks inspect active

### How It Works
1. How It Works
2. Send an image to the API (POST /detect)
3. The request is queued in RabbitMQ
4. A Celery worker picks up the job and runs the TensorFlow model
5. The detection results are sent back via the API

This project is licensed under the MIT License – free to use, modify, and distribute.
