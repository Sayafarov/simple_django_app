FROM python:3.10-slim-bullseye

COPY requirements.txt ./requirements.txt
RUN pip3 install -r ./requirements.txt --no-cache-dir

COPY . /app

ENTRYPOINT ["/app/scripts/entrypoint.sh"]

WORKDIR /app/src

CMD [ "python3 run.py web --collectstatic --no-uvicorn-debug" ]
