# Instrucciones

### Para correr la aplicacion localmente (sin Docker):
```commandline
pip install -r requirements.txt
python init_db.py
uvicorn main:app --reload
```

### Para correr la aplicacion usado Docker:
```commandline
docker-compose up --build
```

Despues de instalar y ejecutar la aplicacion, la documentacion Swagger estara disponible en:

```commandline
http://127.0.0.1:8000/docs
```