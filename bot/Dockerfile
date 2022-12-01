FROM python:3.9.15-alpine

WORKDIR /usr/src/app/
COPY . /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]