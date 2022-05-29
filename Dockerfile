FROM python:3.9.13-alpine3.15

COPY yoshiken_dev_python /app/yoshiken_dev_python
COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

WORKDIR /app

CMD ["python", "-m", "yoshiken_dev_python"]
