FROM python:3.9.13

WORKDIR /app

COPY . .

RUN pip install -r requirments.txt

RUN touch .env

EXPOSE 8000

CMD ["uvicorn", "--port", "8000", "--host", "0.0.0.0", "src.main:app"]