FROM python:3

COPY /requirements.txt /src/meta/requirements.txt

RUN pip install --no-cache-dir -r /src/meta/requirements.txt

WORKDIR /src/app

ENTRYPOINT ["python", "./bot.py"]
