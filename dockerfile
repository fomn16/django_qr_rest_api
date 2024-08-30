FROM python:3.12.5-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN python manage.py collectstatic --no-input --settings=DjangoQrRestApi.settings

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]