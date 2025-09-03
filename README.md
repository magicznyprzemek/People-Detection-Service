## Instalacja:
1. Należy skopiować repozytorium 
2. Umieścić w folderze /models/ plik „frozen_inference_graph.pb” (https://drive.google.com/file/d/1Qc30uGzBU2POIiGgAzSn71XyUP49Gksv/view?usp=share_link)
3. Należy zainstalować redis (https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/)

## Uruchomienie:
1. W terminalu należy wpisać „redis-server” by uruchomić redis
2. W terminalu należy wpisać „uvicorn main:app --host 127.0.0.1 --port 8000 --reload ” by uruchomić fastapi
3. W terminalu należy wpisać „celery -A tasks worker --loglevel=info --concurrency=2 -Q image_queue ” by uruchomić celery, concurrency=x definiuje x równoległych workerów 

## Testowanie:
1. http://127.0.0.1:8000/docs - pozwala sprawdzić api 
2. "celery -A tasks inspect active" - pozwala sprawdzić w terminalu statusy workerów 
