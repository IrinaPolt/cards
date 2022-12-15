FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

CMD ["gunicorn", "cards_project.wsgi:application", "--bind", "0:8000"]