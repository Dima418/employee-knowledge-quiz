FROM python:3.10

WORKDIR /employee-knowledge-quiz

COPY . .

RUN pip3 install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]