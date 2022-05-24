FROM python:3.9.13-alpine3.15

COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

WORKDIR /app

CMD ["python", "main.py"]
