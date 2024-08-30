FROM python:3.12-slim

WORKDIR /app

COPY . .
COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

RUN python -m pytest

# RUN echo "host=''" > ./AUTH.py
# RUN echo "port=''" >> ./AUTH.py
# RUN echo "username=''" >> ./AUTH.py
# RUN echo "password=''" >> ./AUTH.py
# RUN echo "Database=''" >> ./AUTH.py

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app.py
ENV FLASK_ENV development
ENV FLASK_DEBUG 1

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
