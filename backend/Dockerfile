FROM python:3.13

WORKDIR /app

COPY . /app/backend

RUN pip install --no-cache-dir -r /app/backend/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]