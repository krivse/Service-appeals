#FROM python:3.8-slim-buster (debain)
FROM python:3.8-slim
WORKDIR /app
COPY ./requirements.txt /app
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python3", "TornadoHendlers.py"]