FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY app/. .

CMD ["bash", "-c", "ddtrace-run python main.py"]