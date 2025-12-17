FROM python:3.13-slim

WORKDIR /app

RUN pip install Flask pymysql cryptography

COPY . /app

CMD ["python", "Tema2/app.py"]