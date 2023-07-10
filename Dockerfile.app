FROM python:3.10

WORKDIR /employee-knowledge-quiz

COPY ./requirements.txt /employee-knowledge-quiz
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY . /employee-knowledge-quiz

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]