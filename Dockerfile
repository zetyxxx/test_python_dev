FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./db_create.py"]
CMD ["python", "./test.py"]
