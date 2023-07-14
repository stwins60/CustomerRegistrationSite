FROM python:3.7

WORKDIR /app

COPY . .
COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app.py
ENV FLASK_ENV development
ENV FLASK_DEBUG 1

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
