FROM python:3.10

WORKDIR /employee-knowledge-quiz

COPY . /employee-knowledge-quiz/

RUN pip3 install --no-cache-dir --upgrade -r /employee-knowledge-quiz/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]