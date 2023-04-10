FROM python:3.9

LABEL Maintainer='starlingilcruz'

VOLUME ["/usr/app/src"]

WORKDIR /usr/app/src

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV PYTHONUNBUFFERED 1

CMD ["python", "main.py"]

# EXPOSE 8000

# CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]