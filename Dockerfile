FROM python:latest
WORKDIR /app
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip wheel

COPY requirements.txt ./requirements.txt



RUN pip install -r requirements.txt

COPY . .


CMD ["gunicorn", "app.main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4"]

