FROM python:3.9-slim

WORKDIR /app

COPY ./app .

RUN ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "run.py"]