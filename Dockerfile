FROM python:3.9

LABEL Maintainer='starlingilcruz'

VOLUME ["/usr/app/src"]

WORKDIR /usr/app/src

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV PYTHONUNBUFFERED 1

CMD ["python", "main.py"]
