  FROM python:3.10.6-buster
  COPY taxifare taxifare
  COPY requirements.txt requirements.txt
  COPY setup.py setup.py
  RUN pip install --upgrade pip
  RUN pip install -r requirements.txt --use-deprecated=legacy-resolver
  CMD uvicorn taxifare.api.fast:app --host 0.0.0.0 --port $PORT
